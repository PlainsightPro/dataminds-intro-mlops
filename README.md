# dataminds-intro-mlops

Introductory dataMinds session on an intro to MLOps on October 9th 2024.

## About

This GitHub repository contains all content of the dataMinds session on MLOps on October 9th by Nick Verhelst.

The repo is organized in the following folders:

- `src`: This folder contains all demo source code and packages.
- `infra`: This folder contains the TF code to deploy the session infrastructure.

All material and infra used in the session is contained in this repository.

> Note: In the session we focus on DataBricks as a technology. The principles outlined in the talk are however general and can be applied in most ML platforms.

## Getting started

Make sure you meet the following checklist:

- [ ] An Azure subscription. Typically obtained via a free trial or VSE program.
- [ ] Privileges to make resources and resource groups in a given subscription.
- [ ] Rights to manage or create a DataBricks Metastore. 

### 1. Deploying the infrastructure via TerraForm

In order to have a consistent setup the used infrastructure is provided via TerraForm in the `infra` folder.

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

Once you are done with the infrastructure you can run `terraform destroy -var-file="terraform.tfvars` to remove the infrastructure.

> Note: You need to be an account admin on databricks to create the metastore. See the [Azure docs](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/automate).

### 2. Getting started on Databricks

Next you can create a "git folder" in databricks and pull the GitHub repo.

All the code is now in your workspace and you can start experimenting!

You can run the notebooks in the `src` folder one by one. The order to run the notebooks in, is given by their leading number in their name.

To run this code you can spin up an `F4s` compute and run all code there. Make sure to select an ML runtime to have MLflow and the FeatureStore installed.

Have fun!

### 3. Going beyond

In the session we focussed mainly on the general principles on code organization and components of the MLOps framework. We did this by focussing on "how to adjust your project to make it portable".

Note that this was only the beginning of your MLOps journey! If you want to build an MLOps platform you can consult the sources in the References section. These provide great tips and tricks to go to the next level.

## References

The work in this repository is based on the ideas found in the following sources:

- [https://ml-ops.org/](https://ml-ops.org/)
- [https://www.databricks.com/glossary/mlops](https://www.databricks.com/glossary/mlops)
- ["Machine Learning in Production" by Andrew Ng (Deeplearning.ai course, 2024)](https://www.deeplearning.ai/courses/machine-learning-in-production/)
- ["MLOps on databricks: A How to guide (Data+AI Summit 2022)"](https://www.youtube.com/watch?v=DWpy18tz_3U&ab_channel=AcademiadeDados)
- ["MLOps -- End-to-end pipeline" (2022, Databricks)](https://www.databricks.com/resources/demos/tutorials/data-science-and-ai/mlops-end-to-end-pipeline)
- ["Practical MLOps: Operationalizing Machine Learning Models" by Noah Gift and Alfredo Deza (O'Reilly, 2021)](https://www.amazon.com.be/-/nl/Noah-Gift/dp/1098103017/ref=asc_df_1098103017/?tag=begogshpadd0d-21&linkCode=df0&hvadid=633419933432&hvpos=&hvnetw=g&hvrand=305839029236270021&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9197420&hvtargid=pla-1271564395438&psc=1&mcid=8c2c3d289d9532fa978d3fc042e1a9be)
- ["Designing Machine Learning Systems: An iterative Process for Production-Ready Applications" by Chip Huyen (O'Reilly, 2022)](https://www.amazon.com.be/-/en/Chip-Huyen/dp/1098107969/ref=asc_df_1098107969/?tag=begogshpadde-21&linkCode=df0&hvadid=633334843431&hvpos=&hvnetw=g&hvrand=305839029236270021&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9197420&hvtargid=pla-1688018801992&psc=1&mcid=e369280fea543b5f9a3941f71e3bba2f)

Everyone who wants to do a more deep dive on the content of this session, or take the next steps, can find more in the above sources!

## License

This code and content is released under the [unlicense license](https://unlicense.org/).

You are free to do whatever you want with this code: Copy it, sell it, brag at your grandparents. We will not stop you.

Sidenote: The software is provided "as is", without warranty of any kind.

More information can be found in the [license file](LICENSE.md)
