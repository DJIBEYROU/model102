<div align="center">
  <img src="figs/NLR.png" alt="NLR Logo">
</div>

# Contents
- [What is SDOM?](#1-what-is-sdom)
- [Getting started with SDOM](#2-getting-started-with-sdom-and-requirements)
    - [SDOM requirements](#21-System-Setup-and-Prerequisites )
    - [Install SDOM](#22-install-sdom)
- [Next Section - SDOM Inputs](#3-next-section---sdom-inputs)


# 1. What is SDOM?
SDOM (Storage Deployment Optimization Model) is an open-source, high-resolution grid capacity-expansion framework developed by NLR. It’s purpose-built to optimize the storage portfolio considering diverse storage technologies, leveraging hourly temporal resolution and granular spatial representation of Variable Renewable Energy (VRE) sources such as solar and wind.

SDOM is particularly well-suited for figure out the required capacity to meet a carbon-free generation mix target by:
- 📆 Evaluating required optimal short, long-duration and seasonal storage portfolios
- 🌦 Analyzing complementarity and synergies among diverse VRE resources and load profile
- 📉 Assessing curtailment and operational strategies under various grid scenarios

An illustrative figure below shows the flow from inputs to optimization results, enabling exploration of storage needs under varying renewable integration levels.

![SDOM illustrative flow](figs/SDOM_illustration.png)



# 2. Getting started with SDOM
## 2.1 System Setup and Prerequisites 

- a. You'll need to install [python](https://www.python.org/downloads/)
  - After the installation make sure the [python enviroment variable is set](https://realpython.com/add-python-to-path/).
- b. Also, You'll need an IDE (Integrated Development Environment), we recommend to install [MS VS code](https://code.visualstudio.com/)
- c. We also recommend to install extensions such as:
  - [edit CSV](https://marketplace.visualstudio.com/items?itemName=janisdd.vscode-edit-csv): To edit and interact with input csv files for SDOM directly in vs code.
  - [vscode-pdf](https://marketplace.visualstudio.com/items?itemName=tomoki1207.pdf): to read and see pdf files directly in vscode.


## 2.2 Install SDOM

It is recommended to load the packages in a virtual enviroment. 

We recommend to use ``uv``, a Python manager for virtual environments and packages.  


- a. Create a new virtual environment named ``.venv``:

  ```powershell
  uv venv .venv
  ```

  This command creates a Python virtual environment in the ``.venv`` directory.


- b. Activate your virtual environment and install the SDOM package:

  ```powershell
  uv pip install sdom
  ```
        
- c. Install the python module according to your solver. We'll use here [HiGHS open-source solver](https://highs.dev/)
            
  ```powershell
  uv pip install highspy
  ```

- d. Install the Logging package to be able to see sdom info, warning and error messages and log those:

  ```powershell
  uv pip install logging
  ```

- e. Verify your environment by listing installed packages:


  ```powershell
  uv pip list
  ```

    You should see output similar to:
            
  ```
  Package         Version
  --------------- -----------
  highspy         1.11.0
  logging         0.4.9.6
  numpy           2.3.3
  pandas          2.3.3
  ply             3.11
  pyomo           6.9.4
  pytz            2025.2
  sdom            0.0.7
  six             1.17.0
  tzdata          2025.2
  ```

# 3. Next Section - SDOM Inputs
Now, continue to the next section, [SDOM Inputs](training_material\training_sesion_1\1_2_SDOM_Inputs.md)