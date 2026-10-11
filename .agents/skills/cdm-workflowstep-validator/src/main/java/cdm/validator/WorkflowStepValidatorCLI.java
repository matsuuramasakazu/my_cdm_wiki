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
import com.rosetta.model.lib.qualify.QualifyResult;
import com.rosetta.model.lib.validation.ValidationResult;
import org.finos.cdm.CdmRuntimeModule;
import org.finos.cdm.reference.CdmReferenceConfig;
import org.finos.rune.mapper.RuneJsonObjectMapper;

import java.io.File;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

public class WorkflowStepValidatorCLI {

    public static void main(String[] args) {
        if (args.length < 1) {
            System.err.println("Usage: java -jar cdm-workflowstep-validator.jar <path-to-workflowstep.json>");
            System.exit(1);
        }

        String jsonPath = args[0];
        File file = Paths.get(jsonPath).toFile();
        if (!file.exists()) {
            System.err.println("[ERROR] File not found: " + jsonPath);
            System.exit(1);
        }

        int exitCode = validate(file);
        System.exit(exitCode);
    }

    public static int validate(File file) {
        System.out.println("======================================================================");
        System.out.println("                  CDM WORKFLOWSTEP VALIDATION REPORT                  ");
        System.out.println("======================================================================");
        System.out.println("Target File : " + file.getPath());

        // 1. Guice インジェクター初期化 (公式 CDM ランタイムモジュール)
        Injector injector;
        try {
            injector = Guice.createInjector(new CdmRuntimeModule());
        } catch (Exception e) {
            System.err.println("[FATAL] Failed to initialize CDM Guice Injector: " + e.getMessage());
            return 1;
        }

        RosettaTypeValidator typeValidator = injector.getInstance(RosettaTypeValidator.class);
        QualifyProcessorStep qualifyProcessor = injector.getInstance(QualifyProcessorStep.class);

        // 2. Layer 1 & 2: JSON デシリアライズ (CDM v7 Rune JSON または Legacy Rosetta JSON)
        WorkflowStep step = null;
        String detectedFormat = "Unknown";
        Exception deserializationError = null;

        try {
            String content = Files.readString(file.toPath());
            ObjectMapper mapper;
            if (content.contains("\"@type\"") || content.contains("\"@model\"")) {
                mapper = new RuneJsonObjectMapper();
                detectedFormat = "Rune JSON (CDM v7+)";
            } else {
                mapper = RosettaObjectMapper.getNewRosettaObjectMapper();
                detectedFormat = "Legacy Rosetta JSON";
            }

            step = mapper.readValue(file, WorkflowStep.class);
        } catch (Exception e) {
            deserializationError = e;
        }

        if (deserializationError != null || step == null) {
            System.out.println("Overall     : FAIL (Exit Code: 1)");
            System.out.println("Failure Type: JSON Deserialization / Unknown Property / Type Mismatch");
            System.out.println("Error Detail: " + (deserializationError != null ? deserializationError.getMessage() : "Deserialized WorkflowStep is null"));
            System.out.println("======================================================================");
            return 1;
        }

        System.out.println("JSON Format : " + detectedFormat);

        // 3. Layer 3: 内部参照解決 (ReferenceResolverProcessStep)
        WorkflowStep resolvedStep;
        try {
            RosettaModelObject builder = step.toBuilder();
            new ReferenceResolverProcessStep(CdmReferenceConfig.get()).runProcessStep(builder.getType(), builder);
            resolvedStep = (WorkflowStep) builder.build();
        } catch (Exception e) {
            System.out.println("Overall     : FAIL (Exit Code: 1)");
            System.out.println("Failure Type: Reference Resolution Error (meta.globalKey / reference broken)");
            System.out.println("Error Detail: " + e.getMessage());
            System.out.println("======================================================================");
            return 1;
        }

        // 4. Layer 4: Rosetta DSL データルール・条件制約検証 (RosettaTypeValidator)
        ValidationReport validationReport = typeValidator.runProcessStep(WorkflowStep.class, resolvedStep);
        List<ValidationResult<?>> results = validationReport.getValidationResults();

        List<ValidationResult<?>> failures = new ArrayList<>();
        int totalRules = results.size();
        for (ValidationResult<?> r : results) {
            if (!r.isSuccess()) {
                failures.add(r);
            }
        }

        // 5. Layer 5: イベント適格性認定 (QualifyProcessorStep) & 自動突合
        BusinessEvent businessEvent = resolvedStep.getBusinessEvent();
        String declaredQualifier = (businessEvent != null) ? businessEvent.getEventQualifier() : null;
        String intent = (businessEvent != null && businessEvent.getIntent() != null) ? businessEvent.getIntent().name() : null;

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
            } catch (Exception e) {
                System.out.println("[WARN] Qualification processing encountered an error: " + e.getMessage());
            }
        }

        // 突合評価
        boolean eventMatched = true;
        String matchStatus = "N/A";
        if (declaredQualifier != null) {
            // 例: declaredQualifier が "Reset" の場合、Qualify_Reset が含まれるか
            boolean found = qualifiedEventNames.stream().anyMatch(q -> q.toLowerCase().contains(declaredQualifier.toLowerCase()));
            if (found) {
                matchStatus = "MATCH (Declared '" + declaredQualifier + "' matched qualified events)";
            } else {
                eventMatched = false;
                matchStatus = "MISMATCH (Declared '" + declaredQualifier + "' but qualified as " + qualifiedEventNames + ")";
            }
        } else if (qualificationExecuted) {
            if (!qualifiedEventNames.isEmpty()) {
                matchStatus = "INFERRED (Inferred as " + qualifiedEventNames + ")";
            } else {
                matchStatus = "UNQUALIFIED (Warning: No standard CDM qualification matched)";
            }
        }

        // 6. サマリー出力
        boolean isOverallSuccess = failures.isEmpty() && eventMatched;
        System.out.println("Overall     : " + (isOverallSuccess ? "PASS (Exit Code: 0)" : "FAIL (Exit Code: 1)"));
        System.out.println("Step Status : " + (businessEvent != null ? "Accepted (BusinessEvent present)" : (resolvedStep.getProposedEvent() != null ? "Proposed" : "Unknown")));
        System.out.println("Total Rules : " + totalRules + " | Success: " + (totalRules - failures.size()) + " | Failures: " + failures.size());
        if (declaredQualifier != null) System.out.println("Declared Evt: " + declaredQualifier + (intent != null ? " (Intent: " + intent + ")" : ""));
        System.out.println("Qualified   : " + qualifiedEventNames);
        System.out.println("Event Match : " + matchStatus);
        System.out.println("======================================================================");

        // 7. 失敗詳細の出力 (JSON Path, ルール名, failureReason)
        if (!failures.isEmpty()) {
            System.out.println("--- [RULE FAILURES] ---");
            int idx = 1;
            for (ValidationResult<?> f : failures) {
                System.out.println("[" + (idx++) + "] Type  : " + f.getValidationType());
                System.out.println("    Name  : " + f.getName());
                System.out.println("    Model : " + f.getModelObjectName());
                System.out.println("    Path  : " + f.getPath());
                System.out.println("    Reason: " + f.getFailureReason().orElse("None"));
                System.out.println();
            }
            System.out.println("======================================================================");
        }

        return isOverallSuccess ? 0 : 1;
    }
}
