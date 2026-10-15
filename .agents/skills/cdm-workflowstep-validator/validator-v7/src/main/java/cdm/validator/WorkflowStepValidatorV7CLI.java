package cdm.validator;

import cdm.event.common.BusinessEvent;
import cdm.event.workflow.WorkflowStep;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.google.inject.Guice;
import com.google.inject.Injector;
import com.regnosys.rosetta.common.hashing.ReferenceResolverProcessStep;
import com.regnosys.rosetta.common.postprocess.qualify.QualificationReport;
import com.regnosys.rosetta.common.postprocess.qualify.QualifyProcessorStep;
import com.regnosys.rosetta.common.serialisation.RosettaObjectMapper;
import com.regnosys.rosetta.common.validation.RosettaTypeValidator;
import com.regnosys.rosetta.common.validation.ValidationReport;
import com.rosetta.model.lib.RosettaModelObject;
import com.rosetta.model.lib.validation.ValidationResult;
import org.finos.cdm.CdmRuntimeModule;
import org.finos.cdm.reference.CdmReferenceConfig;
import org.finos.rune.mapper.RuneJsonObjectMapper;

import java.io.File;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

public class WorkflowStepValidatorV7CLI {

    public static void main(String[] args) {
        if (args.length < 1) {
            System.err.println("Usage: java -jar cdm-validator-v7.jar <path-to-workflowstep.json>");
            System.exit(1);
        }

        String jsonPath = args[0];
        File file = Paths.get(jsonPath).toFile();
        if (!file.exists()) {
            System.out.println("STATUS   : FAIL (Exit Code: 1)");
            System.out.println("TARGET   : CDM 7.x (v7.5.0)");
            System.out.println("FAILURES :");
            System.out.println("[1] Type  : FILE_NOT_FOUND");
            System.out.println("    Reason: File not found: " + jsonPath);
            System.exit(1);
        }

        int exitCode = validate(file);
        System.exit(exitCode);
    }

    public static int validate(File file) {
        Injector injector;
        try {
            injector = Guice.createInjector(new CdmRuntimeModule());
        } catch (Exception e) {
            System.out.println("STATUS   : FAIL (Exit Code: 1)");
            System.out.println("TARGET   : CDM 7.x (v7.5.0)");
            System.out.println("FAILURES :");
            System.out.println("[1] Type  : INJECTOR_INIT_ERROR");
            System.out.println("    Reason: Failed to initialize CDM Guice Injector: " + e.getMessage());
            return 1;
        }

        RosettaTypeValidator typeValidator = injector.getInstance(RosettaTypeValidator.class);
        QualifyProcessorStep qualifyProcessor = injector.getInstance(QualifyProcessorStep.class);

        WorkflowStep step = null;
        Exception deserializationError = null;

        try {
            String content = Files.readString(file.toPath());
            ObjectMapper mapper;
            if (content.contains("\"@type\"") || content.contains("\"@model\"")) {
                mapper = new RuneJsonObjectMapper();
            } else {
                mapper = RosettaObjectMapper.getNewRosettaObjectMapper();
            }

            step = mapper.readValue(file, WorkflowStep.class);
        } catch (Exception e) {
            deserializationError = e;
        }

        if (deserializationError != null || step == null) {
            System.out.println("STATUS   : FAIL (Exit Code: 1)");
            System.out.println("TARGET   : CDM 7.x (v7.5.0)");
            System.out.println("FAILURES :");
            System.out.println("[1] Type  : DESERIALIZATION_ERROR");
            System.out.println("    Reason: " + (deserializationError != null ? deserializationError.getMessage() : "Deserialized WorkflowStep is null"));
            return 1;
        }

        WorkflowStep resolvedStep;
        try {
            RosettaModelObject builder = step.toBuilder();
            new ReferenceResolverProcessStep(CdmReferenceConfig.get()).runProcessStep(builder.getType(), builder);
            resolvedStep = (WorkflowStep) builder.build();
        } catch (Exception e) {
            System.out.println("STATUS   : FAIL (Exit Code: 1)");
            System.out.println("TARGET   : CDM 7.x (v7.5.0)");
            System.out.println("FAILURES :");
            System.out.println("[1] Type  : REFERENCE_RESOLUTION_ERROR");
            System.out.println("    Reason: Broken globalKey/reference: " + e.getMessage());
            return 1;
        }

        ValidationReport validationReport = typeValidator.runProcessStep(WorkflowStep.class, resolvedStep);
        List<ValidationResult<?>> results = validationReport.getValidationResults();

        List<ValidationResult<?>> failures = new ArrayList<>();
        for (ValidationResult<?> r : results) {
            if (!r.isSuccess()) {
                failures.add(r);
            }
        }

        BusinessEvent businessEvent = resolvedStep.getBusinessEvent();
        String declaredQualifier = (businessEvent != null) ? businessEvent.getEventQualifier() : null;

        List<String> qualifiedEventNames = new ArrayList<>();
        boolean qualificationExecuted = false;

        if (businessEvent != null) {
            qualificationExecuted = true;
            try {
                QualificationReport qualReport = qualifyProcessor.runProcessStep(BusinessEvent.class, businessEvent.toBuilder());
                qualReport.getResults().forEach(res -> {
                    String typeName = res.getQualifiedRosettaObjectType().getSimpleName();
                    if (typeName.equalsIgnoreCase(BusinessEvent.class.getSimpleName())) {
                        res.getUniqueSuccessQualifyResult().ifPresent(qr -> qualifiedEventNames.add(qr.getName()));
                    }
                });
            } catch (Exception ignored) {
            }
        }

        boolean eventMatched = true;
        String qualSummary = "None";
        if (declaredQualifier != null) {
            boolean found = qualifiedEventNames.stream().anyMatch(q -> q.toLowerCase().contains(declaredQualifier.toLowerCase()));
            if (found) {
                qualSummary = declaredQualifier + " (MATCH)";
            } else {
                eventMatched = false;
                qualSummary = declaredQualifier + " (MISMATCH: qualified as " + qualifiedEventNames + ")";
            }
        } else if (qualificationExecuted) {
            if (!qualifiedEventNames.isEmpty()) {
                qualSummary = qualifiedEventNames.toString() + " (INFERRED)";
            } else {
                qualSummary = "UNQUALIFIED";
            }
        } else {
            qualSummary = "N/A (Step: " + (resolvedStep.getProposedEvent() != null ? "Proposed" : "Accepted") + ")";
        }

        boolean isOverallSuccess = failures.isEmpty() && eventMatched;

        if (isOverallSuccess) {
            System.out.println("STATUS   : PASS (Exit Code: 0)");
            System.out.println("MODEL    : CDM 7.x (v7.5.0)");
            System.out.println("QUALIFIED: " + qualSummary);
            return 0;
        } else {
            System.out.println("STATUS   : FAIL (Exit Code: 1)");
            System.out.println("TARGET   : CDM 7.x (v7.5.0)");
            System.out.println("FAILURES :");
            int idx = 1;
            if (!eventMatched) {
                System.out.println("[" + (idx++) + "] Type  : EVENT_QUALIFICATION_MISMATCH");
                System.out.println("    Reason: Declared '" + declaredQualifier + "' but qualified as " + qualifiedEventNames);
            }
            for (ValidationResult<?> f : failures) {
                System.out.println("[" + (idx++) + "] Path  : " + f.getPath());
                System.out.println("    Rule  : " + f.getName() + " (" + f.getValidationType() + ")");
                System.out.println("    Reason: " + f.getFailureReason().orElse("Condition or cardinality requirement unsatisfied"));
            }
            return 1;
        }
    }
}
