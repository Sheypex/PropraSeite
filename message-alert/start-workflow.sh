#!/usr/bin/env bash

echo 'Starting the workflow'
knime -nosplash -application org.knime.product.KNIME_BATCH_APPLICATION -workflowDir="./message_alert_system"
echo 'Finished the workflow execution... '