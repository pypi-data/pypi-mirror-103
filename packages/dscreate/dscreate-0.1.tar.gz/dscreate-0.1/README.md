# dscreate
> Flatiron School Data Science Tools

## Installation
This package is not currently hosted on PyPi but is compatible with `pip`. 

**To install**
1. Clone this repository 
2. Navigate into this project directory
3. run `pip install .` in command line.


## Available Tools
#### `ds -begin`
When this command is run the following things happen:
1. A `data` folder is added to the current working directory
2. A `.solution_files` subdirectory is added to the current working directory
3. A `curriculum.ipynb` file is added to the current working directory
   - This notebook contains instructions  for creating solution tags
   - All curriculum content needs to be created in this file in order to use `ds -create`.

#### `ds -create`
When this command is run the following things happen
1. An `index.ipynb` file is added to the current working directory containing all "student facing" content within the `curriculum.ipynb` file
2. An `index.ipynb` file is added to the `.solution_files` subdirectory containing all solution content in the `curriculum.ipynb` file.
3. This file structure is designed to be compatible with the file structure for resources in the [Cohort Lead Repository](https://github.com/learn-co-students/cohort-lead-repository)

*Brief note:*

After running this command, if you are pushing materials for a lesson, it is recommended that you do not run `git add .`

Instead, it is recommended that you add files manually to avoid sharing the solution with students. 

*Example*
```
git add index.ipynb data/
git commit -m 'commit message'
git push origin master
```


#### `ds -share <github notebook url>`
This command accepts any link that points to a public notebook on github. When this command is run, a link is copied to your clipboard that points to the notebook on illumidesk. 
- This command can be used to create [url module items](https://community.canvaslms.com/t5/Instructor-Guide/How-do-I-add-an-external-URL-as-a-module-item/ta-p/967) in canvas
- This command can be used with the [Cohort Lead Repository](https://github.com/learn-co-students/cohort-lead-repository) to facilitate coding exercises during 1:1s and other live sessions.

