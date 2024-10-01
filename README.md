# dataminds-intro-mlops

Introductory dataMinds session on an intro to MLOps on October 9th 2024.

## About

This GitHub repository contains all content of the dataMinds session on MLOps on October 9th by Nick Verhelst.

## Getting started

Make sure you meet the following checklist:
[] An Azure subscription. Typically obtained via a free trial or VSE program.

### Deploying the infrastructure via TerraForm

In order to have a consistent setup the used infrastructure is provided via TerraForm.

This includes the following resources:

- A databricks workspace
- A storage account with hierarchical namespace enabled
- A Unity Catalog account coupled to this storage account and databricks.

In order to have this deployment automated you should first [install terraform following their instructions](https://developer.hashicorp.com/terraform/tutorials/azure-get-started/install-cli).

Once installed you need to run following steps:

0. `cd` into the `infra` folder. Here you will have all needed code.
1. Change the `terraform.tfvars` to have your variables in there.
2. Run `terraform init`: This downloads all required providers.
3. (optional) Run `terraform plan -var-file="terraform.tfvars"`: This will validate your setup and show you all the changes that are about to be made.
4. Run `terraform plan -var-file="terraform.tfvars"`: This will deploy all infrastructure to your Azure subscription in a resource group `rg-<prefix>-<project_name>` in the region `region` as specified in the tfvars. The deploy should take around 5 minutes to complete.

Congratulations, your infrastructure is now completely set up!

Once you are done you can run `terraform destroy -var-file="terraform.tfvars` to remove the infrastructure.

> Note: You need to be an account admin on databricks to create the metastore. See the [Azure docs](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/automate).

## References

The work in this repository is based on the ideas found in the following sources:

- [https://ml-ops.org/](https://ml-ops.org/)
- [https://www.databricks.com/glossary/mlops](https://www.databricks.com/glossary/mlops)
- ["Machine Learning in Production" by Andrew Ng (Deeplearning.ai course, 2024)](https://www.deeplearning.ai/courses/machine-learning-in-production/)
- ["End to End ML Project" by Beau Carnes (FreeCodeCamp, 2024)](https://www.freecodecamp.org/news/end-to-end-machine-learning-course-project/)
- ["Practical MLOps: Operationalizing Machine Learning Models" by Noah Gift and Alfredo Deza (O'Reilly, 2021)](https://www.amazon.com.be/-/nl/Noah-Gift/dp/1098103017/ref=asc_df_1098103017/?tag=begogshpadd0d-21&linkCode=df0&hvadid=633419933432&hvpos=&hvnetw=g&hvrand=305839029236270021&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9197420&hvtargid=pla-1271564395438&psc=1&mcid=8c2c3d289d9532fa978d3fc042e1a9be)
- ["Designing Machine Learning Systems: An iterative Process for Production-Ready Applications" by Chip Huyen (O'Reilly, 2022)](https://www.amazon.com.be/-/en/Chip-Huyen/dp/1098107969/ref=asc_df_1098107969/?tag=begogshpadde-21&linkCode=df0&hvadid=633334843431&hvpos=&hvnetw=g&hvrand=305839029236270021&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9197420&hvtargid=pla-1688018801992&psc=1&mcid=e369280fea543b5f9a3941f71e3bba2f)

## License

This code and content is released under the [unlicense license](https://unlicense.org/).

You are free to do whatever you want with this code: Copy it, sell it, brag at your grandparents. We will not stop you.

Sidenote: The software is provided "as is", without warranty of any kind.

More information can be found in the [license file](LICENSE.md)
