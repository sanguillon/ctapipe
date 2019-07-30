{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Test of provenance\n",
    "\n",
    "## Objective\n",
    "- The goal of this test is to have an idea of the existing tools to implement the provenance in a program of CTA using the ctapipe library\n",
    "\n",
    "## Context\n",
    "- This test is done with the muon_reconstruction.py program \n",
    "- This program uses ctapipe and provenance modules/libraries (v. 0.6.2.post150+gita494195)\n",
    "- The Provenance database is defined in memory and accessed with the sqlalchemy library\n",
    "\n",
    "## Structure of the notebook\n",
    "- Definition the Provenance database structure\n",
    "- Definition of the muon_reconstruction tool\n",
    "- Addition of the muon_reconstruction (named ctapipe_display_muons) activity description in the provenance database\n",
    "- Execution of the muon_reconstruction program\n",
    "- Addition of the provenance information of the job in the database\n",
    "- Query the provenance database and store the result in a file\n",
    "- Vizualisation of the provenance\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Definition of the Provenance database structure\n",
    "\n",
    "#### Provenance Data Model PR2 2019-07-19\n",
    "<img src=\"2019-07-19_PR2_PROV_Fig8.png\">\n",
    "\n",
    "#### Remarks\n",
    "- Activity\n",
    "    Activity.activityDescription = concat(activity_name, '_', ctapipe_version)\n",
    "    Dates are curreuntly stored as strings\n",
    "- Entity\n",
    "    Entity.id = hash(file)\n",
    "    Inheritance is implemented as joined table inheritance (dependant tables) => addition of the classType attribute in the Entity and EntityDescription classes\n",
    "- Relations\n",
    "    Used.id, WasGeneratedBy.id, WasAttributedTo.id, WasAssociatedWith.id are interger and autoincremented\n",
    "- A lot of empty fields and problem to associate Entity with EntityDescription\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-07-30 11:02:12,464 INFO sqlalchemy.engine.base.Engine SELECT CAST('test plain returns' AS VARCHAR(60)) AS anon_1\n",
      "2019-07-30 11:02:12,465 INFO sqlalchemy.engine.base.Engine ()\n",
      "2019-07-30 11:02:12,466 INFO sqlalchemy.engine.base.Engine SELECT CAST('test unicode returns' AS VARCHAR(60)) AS anon_1\n",
      "2019-07-30 11:02:12,467 INFO sqlalchemy.engine.base.Engine ()\n",
      "2019-07-30 11:02:12,468 INFO sqlalchemy.engine.base.Engine PRAGMA table_info(\"wasInformedBy\")\n",
      "2019-07-30 11:02:12,469 INFO sqlalchemy.engine.base.Engine ()\n",
      "2019-07-30 11:02:12,471 INFO sqlalchemy.engine.base.Engine PRAGMA table_info(\"activities\")\n",
      "2019-07-30 11:02:12,471 INFO sqlalchemy.engine.base.Engine ()\n",
      "2019-07-30 11:02:12,472 INFO sqlalchemy.engine.base.Engine PRAGMA table_info(\"wasDerivedFrom\")\n",
      "2019-07-30 11:02:12,473 INFO sqlalchemy.engine.base.Engine ()\n",
      "2019-07-30 11:02:12,474 INFO sqlalchemy.engine.base.Engine PRAGMA table_info(\"entities\")\n",
      "2019-07-30 11:02:12,475 INFO sqlalchemy.engine.base.Engine ()\n",
      "2019-07-30 11:02:12,476 INFO sqlalchemy.engine.base.Engine PRAGMA table_info(\"used\")\n",
      "2019-07-30 11:02:12,476 INFO sqlalchemy.engine.base.Engine ()\n",
      "2019-07-30 11:02:12,477 INFO sqlalchemy.engine.base.Engine PRAGMA table_info(\"wasGeneratedBy\")\n",
      "2019-07-30 11:02:12,478 INFO sqlalchemy.engine.base.Engine ()\n",
      "2019-07-30 11:02:12,479 INFO sqlalchemy.engine.base.Engine PRAGMA table_info(\"valueEntities\")\n",
      "2019-07-30 11:02:12,479 INFO sqlalchemy.engine.base.Engine ()\n",
      "2019-07-30 11:02:12,480 INFO sqlalchemy.engine.base.Engine PRAGMA table_info(\"datasetEntities\")\n",
      "2019-07-30 11:02:12,481 INFO sqlalchemy.engine.base.Engine ()\n",
      "2019-07-30 11:02:12,482 INFO sqlalchemy.engine.base.Engine PRAGMA table_info(\"agents\")\n",
      "2019-07-30 11:02:12,483 INFO sqlalchemy.engine.base.Engine ()\n",
      "2019-07-30 11:02:12,484 INFO sqlalchemy.engine.base.Engine PRAGMA table_info(\"wasAssociatedWith\")\n",
      "2019-07-30 11:02:12,485 INFO sqlalchemy.engine.base.Engine ()\n",
      "2019-07-30 11:02:12,485 INFO sqlalchemy.engine.base.Engine PRAGMA table_info(\"wasAttributedTo\")\n",
      "2019-07-30 11:02:12,486 INFO sqlalchemy.engine.base.Engine ()\n",
      "2019-07-30 11:02:12,488 INFO sqlalchemy.engine.base.Engine PRAGMA table_info(\"activityDescriptions\")\n",
      "2019-07-30 11:02:12,488 INFO sqlalchemy.engine.base.Engine ()\n",
      "2019-07-30 11:02:12,490 INFO sqlalchemy.engine.base.Engine PRAGMA table_info(\"entityDescriptions\")\n",
      "2019-07-30 11:02:12,490 INFO sqlalchemy.engine.base.Engine ()\n",
      "2019-07-30 11:02:12,491 INFO sqlalchemy.engine.base.Engine PRAGMA table_info(\"usageDescriptions\")\n",
      "2019-07-30 11:02:12,492 INFO sqlalchemy.engine.base.Engine ()\n",
      "2019-07-30 11:02:12,496 INFO sqlalchemy.engine.base.Engine PRAGMA table_info(\"generationDescriptions\")\n",
      "2019-07-30 11:02:12,499 INFO sqlalchemy.engine.base.Engine ()\n",
      "2019-07-30 11:02:12,502 INFO sqlalchemy.engine.base.Engine PRAGMA table_info(\"valueDescriptions\")\n",
      "2019-07-30 11:02:12,502 INFO sqlalchemy.engine.base.Engine ()\n",
      "2019-07-30 11:02:12,503 INFO sqlalchemy.engine.base.Engine PRAGMA table_info(\"datasetDescriptions\")\n",
      "2019-07-30 11:02:12,504 INFO sqlalchemy.engine.base.Engine ()\n",
      "2019-07-30 11:02:12,505 INFO sqlalchemy.engine.base.Engine PRAGMA table_info(\"parameters\")\n",
      "2019-07-30 11:02:12,506 INFO sqlalchemy.engine.base.Engine ()\n",
      "2019-07-30 11:02:12,507 INFO sqlalchemy.engine.base.Engine PRAGMA table_info(\"parameterDescriptions\")\n",
      "2019-07-30 11:02:12,508 INFO sqlalchemy.engine.base.Engine ()\n",
      "2019-07-30 11:02:12,509 INFO sqlalchemy.engine.base.Engine PRAGMA table_info(\"configFiles\")\n",
      "2019-07-30 11:02:12,512 INFO sqlalchemy.engine.base.Engine ()\n",
      "2019-07-30 11:02:12,514 INFO sqlalchemy.engine.base.Engine PRAGMA table_info(\"configFileDescriptions\")\n",
      "2019-07-30 11:02:12,516 INFO sqlalchemy.engine.base.Engine ()\n",
      "2019-07-30 11:02:12,518 INFO sqlalchemy.engine.base.Engine PRAGMA table_info(\"wasConfiguredBy\")\n",
      "2019-07-30 11:02:12,523 INFO sqlalchemy.engine.base.Engine ()\n",
      "2019-07-30 11:02:12,527 INFO sqlalchemy.engine.base.Engine \n",
      "CREATE TABLE agents (\n",
      "\tid VARCHAR NOT NULL, \n",
      "\tname VARCHAR, \n",
      "\ttype VARCHAR, \n",
      "\temail VARCHAR, \n",
      "\taffiliation VARCHAR, \n",
      "\tphone VARCHAR, \n",
      "\taddress VARCHAR, \n",
      "\tcomment VARCHAR, \n",
      "\turl VARCHAR, \n",
      "\tPRIMARY KEY (id)\n",
      ")\n",
      "\n",
      "\n",
      "2019-07-30 11:02:12,528 INFO sqlalchemy.engine.base.Engine ()\n",
      "2019-07-30 11:02:12,529 INFO sqlalchemy.engine.base.Engine COMMIT\n",
      "2019-07-30 11:02:12,530 INFO sqlalchemy.engine.base.Engine \n",
      "CREATE TABLE \"activityDescriptions\" (\n",
      "\tid VARCHAR NOT NULL, \n",
      "\tname VARCHAR, \n",
      "\tversion VARCHAR, \n",
      "\tdescription VARCHAR, \n",
      "\ttype VARCHAR, \n",
      "\tsubtype VARCHAR, \n",
      "\tdoculink VARCHAR, \n",
      "\tPRIMARY KEY (id)\n",
      ")\n",
      "\n",
      "\n",
      "2019-07-30 11:02:12,531 INFO sqlalchemy.engine.base.Engine ()\n",
      "2019-07-30 11:02:12,532 INFO sqlalchemy.engine.base.Engine COMMIT\n",
      "2019-07-30 11:02:12,533 INFO sqlalchemy.engine.base.Engine \n",
      "CREATE TABLE \"entityDescriptions\" (\n",
      "\tid VARCHAR NOT NULL, \n",
      "\tname VARCHAR, \n",
      "\ttype VARCHAR, \n",
      "\tdescription VARCHAR, \n",
      "\tdoculink VARCHAR, \n",
      "\t\"classType\" VARCHAR, \n",
      "\tPRIMARY KEY (id)\n",
      ")\n",
      "\n",
      "\n",
      "2019-07-30 11:02:12,534 INFO sqlalchemy.engine.base.Engine ()\n",
      "2019-07-30 11:02:12,535 INFO sqlalchemy.engine.base.Engine COMMIT\n",
      "2019-07-30 11:02:12,536 INFO sqlalchemy.engine.base.Engine \n",
      "CREATE TABLE activities (\n",
      "\tid VARCHAR NOT NULL, \n",
      "\tname VARCHAR, \n",
      "\t\"startTime\" VARCHAR, \n",
      "\t\"endTime\" VARCHAR, \n",
      "\tcomment VARCHAR, \n",
      "\t\"activityDescription_id\" VARCHAR, \n",
      "\tPRIMARY KEY (id), \n",
      "\tFOREIGN KEY(\"activityDescription_id\") REFERENCES \"activityDescriptions\" (id)\n",
      ")\n",
      "\n",
      "\n",
      "2019-07-30 11:02:12,537 INFO sqlalchemy.engine.base.Engine ()\n",
      "2019-07-30 11:02:12,538 INFO sqlalchemy.engine.base.Engine COMMIT\n",
      "2019-07-30 11:02:12,539 INFO sqlalchemy.engine.base.Engine \n",
      "CREATE TABLE entities (\n",
      "\tid VARCHAR NOT NULL, \n",
      "\tname VARCHAR, \n",
      "\tlocation VARCHAR, \n",
      "\t\"generatedAtTime\" VARCHAR, \n",
      "\t\"invalidatedAtTime\" VARCHAR, \n",
      "\tcomment VARCHAR, \n",
      "\t\"entityDescription_id\" VARCHAR, \n",
      "\t\"classType\" VARCHAR, \n",
      "\tPRIMARY KEY (id), \n",
      "\tFOREIGN KEY(\"entityDescription_id\") REFERENCES \"entityDescriptions\" (id)\n",
      ")\n",
      "\n",
      "\n",
      "2019-07-30 11:02:12,540 INFO sqlalchemy.engine.base.Engine ()\n",
      "2019-07-30 11:02:12,541 INFO sqlalchemy.engine.base.Engine COMMIT\n",
      "2019-07-30 11:02:12,543 INFO sqlalchemy.engine.base.Engine \n",
      "CREATE TABLE \"usageDescriptions\" (\n",
      "\tid VARCHAR NOT NULL, \n",
      "\trole VARCHAR, \n",
      "\tdescription VARCHAR, \n",
      "\ttype VARCHAR, \n",
      "\tmultiplicity INTEGER, \n",
      "\t\"activityDescription_id\" VARCHAR, \n",
      "\t\"entityDescription_id\" VARCHAR, \n",
      "\tPRIMARY KEY (id), \n",
      "\tFOREIGN KEY(\"activityDescription_id\") REFERENCES \"activityDescriptions\" (id), \n",
      "\tFOREIGN KEY(\"entityDescription_id\") REFERENCES \"entityDescriptions\" (id)\n",
      ")\n",
      "\n",
      "\n",
      "2019-07-30 11:02:12,544 INFO sqlalchemy.engine.base.Engine ()\n",
      "2019-07-30 11:02:12,545 INFO sqlalchemy.engine.base.Engine COMMIT\n",
      "2019-07-30 11:02:12,546 INFO sqlalchemy.engine.base.Engine \n",
      "CREATE TABLE \"generationDescriptions\" (\n",
      "\tid VARCHAR NOT NULL, \n",
      "\trole VARCHAR, \n",
      "\tdescription VARCHAR, \n",
      "\ttype VARCHAR, \n",
      "\tmultiplicity INTEGER, \n",
      "\t\"activityDescription_id\" VARCHAR, \n",
      "\t\"entityDescription_id\" VARCHAR, \n",
      "\tPRIMARY KEY (id), \n",
      "\tFOREIGN KEY(\"activityDescription_id\") REFERENCES \"activityDescriptions\" (id), \n",
      "\tFOREIGN KEY(\"entityDescription_id\") REFERENCES \"entityDescriptions\" (id)\n",
      ")\n",
      "\n",
      "\n",
      "2019-07-30 11:02:12,546 INFO sqlalchemy.engine.base.Engine ()\n",
      "2019-07-30 11:02:12,547 INFO sqlalchemy.engine.base.Engine COMMIT\n",
      "2019-07-30 11:02:12,548 INFO sqlalchemy.engine.base.Engine \n",
      "CREATE TABLE \"valueDescriptions\" (\n",
      "\tid VARCHAR NOT NULL, \n",
      "\t\"valueType\" VARCHAR, \n",
      "\tunit VARCHAR, \n",
      "\tucd VARCHAR, \n",
      "\tutype VARCHAR, \n",
      "\tmin VARCHAR, \n",
      "\tmax VARCHAR, \n",
      "\t\"default\" VARCHAR, \n",
      "\toptions VARCHAR, \n",
      "\tPRIMARY KEY (id), \n",
      "\tFOREIGN KEY(id) REFERENCES \"entityDescriptions\" (id)\n",
      ")\n",
      "\n",
      "\n",
      "2019-07-30 11:02:12,549 INFO sqlalchemy.engine.base.Engine ()\n",
      "2019-07-30 11:02:12,550 INFO sqlalchemy.engine.base.Engine COMMIT\n",
      "2019-07-30 11:02:12,551 INFO sqlalchemy.engine.base.Engine \n",
      "CREATE TABLE \"datasetDescriptions\" (\n",
      "\tid VARCHAR NOT NULL, \n",
      "\t\"contentType\" VARCHAR, \n",
      "\tPRIMARY KEY (id), \n",
      "\tFOREIGN KEY(id) REFERENCES \"entityDescriptions\" (id)\n",
      ")\n",
      "\n",
      "\n",
      "2019-07-30 11:02:12,551 INFO sqlalchemy.engine.base.Engine ()\n",
      "2019-07-30 11:02:12,553 INFO sqlalchemy.engine.base.Engine COMMIT\n",
      "2019-07-30 11:02:12,554 INFO sqlalchemy.engine.base.Engine \n",
      "CREATE TABLE \"wasInformedBy\" (\n",
      "\t\"wasInformedBy_Id\" INTEGER NOT NULL, \n",
      "\tinformant VARCHAR, \n",
      "\tinformed VARCHAR, \n",
      "\tPRIMARY KEY (\"wasInformedBy_Id\"), \n",
      "\tFOREIGN KEY(informant) REFERENCES activities (id), \n",
      "\tFOREIGN KEY(informed) REFERENCES activities (id)\n",
      ")\n",
      "\n",
      "\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-07-30 11:02:12,554 INFO sqlalchemy.engine.base.Engine ()\n",
      "2019-07-30 11:02:12,555 INFO sqlalchemy.engine.base.Engine COMMIT\n",
      "2019-07-30 11:02:12,556 INFO sqlalchemy.engine.base.Engine \n",
      "CREATE TABLE \"wasDerivedFrom\" (\n",
      "\t\"generatedEntity\" VARCHAR, \n",
      "\t\"usedEntity\" VARCHAR, \n",
      "\tFOREIGN KEY(\"generatedEntity\") REFERENCES entities (id), \n",
      "\tFOREIGN KEY(\"usedEntity\") REFERENCES entities (id)\n",
      ")\n",
      "\n",
      "\n",
      "2019-07-30 11:02:12,557 INFO sqlalchemy.engine.base.Engine ()\n",
      "2019-07-30 11:02:12,558 INFO sqlalchemy.engine.base.Engine COMMIT\n",
      "2019-07-30 11:02:12,559 INFO sqlalchemy.engine.base.Engine \n",
      "CREATE TABLE used (\n",
      "\tid INTEGER NOT NULL, \n",
      "\trole VARCHAR, \n",
      "\ttime VARCHAR, \n",
      "\tactivity_id VARCHAR, \n",
      "\tentity_id VARCHAR, \n",
      "\t\"usageDescription_id\" VARCHAR, \n",
      "\tPRIMARY KEY (id), \n",
      "\tFOREIGN KEY(activity_id) REFERENCES activities (id), \n",
      "\tFOREIGN KEY(entity_id) REFERENCES entities (id), \n",
      "\tFOREIGN KEY(\"usageDescription_id\") REFERENCES \"usageDescriptions\" (id)\n",
      ")\n",
      "\n",
      "\n",
      "2019-07-30 11:02:12,559 INFO sqlalchemy.engine.base.Engine ()\n",
      "2019-07-30 11:02:12,560 INFO sqlalchemy.engine.base.Engine COMMIT\n",
      "2019-07-30 11:02:12,561 INFO sqlalchemy.engine.base.Engine \n",
      "CREATE TABLE \"wasGeneratedBy\" (\n",
      "\tid INTEGER NOT NULL, \n",
      "\trole VARCHAR, \n",
      "\tactivity_id VARCHAR, \n",
      "\tentity_id VARCHAR, \n",
      "\t\"generationDescription_id\" VARCHAR, \n",
      "\tPRIMARY KEY (id), \n",
      "\tFOREIGN KEY(activity_id) REFERENCES activities (id), \n",
      "\tFOREIGN KEY(entity_id) REFERENCES entities (id), \n",
      "\tFOREIGN KEY(\"generationDescription_id\") REFERENCES \"generationDescriptions\" (id)\n",
      ")\n",
      "\n",
      "\n",
      "2019-07-30 11:02:12,561 INFO sqlalchemy.engine.base.Engine ()\n",
      "2019-07-30 11:02:12,562 INFO sqlalchemy.engine.base.Engine COMMIT\n",
      "2019-07-30 11:02:12,563 INFO sqlalchemy.engine.base.Engine \n",
      "CREATE TABLE \"valueEntities\" (\n",
      "\tid VARCHAR NOT NULL, \n",
      "\tvalue VARCHAR, \n",
      "\tPRIMARY KEY (id), \n",
      "\tFOREIGN KEY(id) REFERENCES entities (id)\n",
      ")\n",
      "\n",
      "\n",
      "2019-07-30 11:02:12,564 INFO sqlalchemy.engine.base.Engine ()\n",
      "2019-07-30 11:02:12,565 INFO sqlalchemy.engine.base.Engine COMMIT\n",
      "2019-07-30 11:02:12,566 INFO sqlalchemy.engine.base.Engine \n",
      "CREATE TABLE \"datasetEntities\" (\n",
      "\tid VARCHAR NOT NULL, \n",
      "\tPRIMARY KEY (id), \n",
      "\tFOREIGN KEY(id) REFERENCES entities (id)\n",
      ")\n",
      "\n",
      "\n",
      "2019-07-30 11:02:12,567 INFO sqlalchemy.engine.base.Engine ()\n",
      "2019-07-30 11:02:12,568 INFO sqlalchemy.engine.base.Engine COMMIT\n",
      "2019-07-30 11:02:12,568 INFO sqlalchemy.engine.base.Engine \n",
      "CREATE TABLE \"wasAssociatedWith\" (\n",
      "\tid INTEGER NOT NULL, \n",
      "\trole VARCHAR, \n",
      "\tactivity VARCHAR, \n",
      "\tagent VARCHAR, \n",
      "\tPRIMARY KEY (id), \n",
      "\tFOREIGN KEY(activity) REFERENCES activities (id), \n",
      "\tFOREIGN KEY(agent) REFERENCES agents (id)\n",
      ")\n",
      "\n",
      "\n",
      "2019-07-30 11:02:12,569 INFO sqlalchemy.engine.base.Engine ()\n",
      "2019-07-30 11:02:12,570 INFO sqlalchemy.engine.base.Engine COMMIT\n",
      "2019-07-30 11:02:12,570 INFO sqlalchemy.engine.base.Engine \n",
      "CREATE TABLE \"wasAttributedTo\" (\n",
      "\tid INTEGER NOT NULL, \n",
      "\trole VARCHAR, \n",
      "\tentity VARCHAR, \n",
      "\tagent VARCHAR, \n",
      "\tPRIMARY KEY (id), \n",
      "\tFOREIGN KEY(entity) REFERENCES entities (id), \n",
      "\tFOREIGN KEY(agent) REFERENCES agents (id)\n",
      ")\n",
      "\n",
      "\n",
      "2019-07-30 11:02:12,571 INFO sqlalchemy.engine.base.Engine ()\n",
      "2019-07-30 11:02:12,572 INFO sqlalchemy.engine.base.Engine COMMIT\n",
      "2019-07-30 11:02:12,573 INFO sqlalchemy.engine.base.Engine \n",
      "CREATE TABLE \"parameterDescriptions\" (\n",
      "\tid VARCHAR NOT NULL, \n",
      "\tname VARCHAR, \n",
      "\t\"valueType\" VARCHAR, \n",
      "\tunit VARCHAR, \n",
      "\tucd VARCHAR, \n",
      "\tutype VARCHAR, \n",
      "\tmin VARCHAR, \n",
      "\tmax VARCHAR, \n",
      "\toptions VARCHAR, \n",
      "\t\"default\" VARCHAR, \n",
      "\tdescription VARCHAR, \n",
      "\tPRIMARY KEY (id), \n",
      "\tFOREIGN KEY(id) REFERENCES \"valueDescriptions\" (id)\n",
      ")\n",
      "\n",
      "\n",
      "2019-07-30 11:02:12,574 INFO sqlalchemy.engine.base.Engine ()\n",
      "2019-07-30 11:02:12,574 INFO sqlalchemy.engine.base.Engine COMMIT\n",
      "2019-07-30 11:02:12,575 INFO sqlalchemy.engine.base.Engine \n",
      "CREATE TABLE \"configFileDescriptions\" (\n",
      "\tid VARCHAR NOT NULL, \n",
      "\tname VARCHAR, \n",
      "\t\"contextType\" VARCHAR, \n",
      "\tdescription VARCHAR, \n",
      "\tPRIMARY KEY (id), \n",
      "\tFOREIGN KEY(id) REFERENCES \"valueDescriptions\" (id)\n",
      ")\n",
      "\n",
      "\n",
      "2019-07-30 11:02:12,577 INFO sqlalchemy.engine.base.Engine ()\n",
      "2019-07-30 11:02:12,578 INFO sqlalchemy.engine.base.Engine COMMIT\n",
      "2019-07-30 11:02:12,579 INFO sqlalchemy.engine.base.Engine \n",
      "CREATE TABLE parameters (\n",
      "\tid VARCHAR NOT NULL, \n",
      "\tvalue VARCHAR, \n",
      "\tname VARCHAR, \n",
      "\t\"parameterDescription_id\" VARCHAR, \n",
      "\tPRIMARY KEY (id), \n",
      "\tFOREIGN KEY(id) REFERENCES \"valueEntities\" (id), \n",
      "\tFOREIGN KEY(\"parameterDescription_id\") REFERENCES \"parameterDescriptions\" (id)\n",
      ")\n",
      "\n",
      "\n",
      "2019-07-30 11:02:12,580 INFO sqlalchemy.engine.base.Engine ()\n",
      "2019-07-30 11:02:12,581 INFO sqlalchemy.engine.base.Engine COMMIT\n",
      "2019-07-30 11:02:12,582 INFO sqlalchemy.engine.base.Engine \n",
      "CREATE TABLE \"configFiles\" (\n",
      "\tid VARCHAR NOT NULL, \n",
      "\tname VARCHAR, \n",
      "\tlocation VARCHAR, \n",
      "\tcomment VARCHAR, \n",
      "\t\"configFileDescription_id\" VARCHAR, \n",
      "\t\"parameterDescription_id\" VARCHAR, \n",
      "\tPRIMARY KEY (id), \n",
      "\tFOREIGN KEY(id) REFERENCES \"valueEntities\" (id), \n",
      "\tFOREIGN KEY(\"configFileDescription_id\") REFERENCES \"configFileDescriptions\" (id), \n",
      "\tFOREIGN KEY(\"parameterDescription_id\") REFERENCES \"parameterDescriptions\" (id)\n",
      ")\n",
      "\n",
      "\n",
      "2019-07-30 11:02:12,583 INFO sqlalchemy.engine.base.Engine ()\n",
      "2019-07-30 11:02:12,584 INFO sqlalchemy.engine.base.Engine COMMIT\n",
      "2019-07-30 11:02:12,584 INFO sqlalchemy.engine.base.Engine \n",
      "CREATE TABLE \"wasConfiguredBy\" (\n",
      "\tid INTEGER NOT NULL, \n",
      "\t\"artefactType\" VARCHAR, \n",
      "\tactivity_id VARCHAR, \n",
      "\tparameter_id VARCHAR, \n",
      "\t\"configFile_id\" VARCHAR, \n",
      "\tPRIMARY KEY (id), \n",
      "\tFOREIGN KEY(activity_id) REFERENCES activities (id), \n",
      "\tFOREIGN KEY(parameter_id) REFERENCES parameters (id), \n",
      "\tFOREIGN KEY(\"configFile_id\") REFERENCES \"configFiles\" (id)\n",
      ")\n",
      "\n",
      "\n",
      "2019-07-30 11:02:12,585 INFO sqlalchemy.engine.base.Engine ()\n",
      "2019-07-30 11:02:12,586 INFO sqlalchemy.engine.base.Engine COMMIT\n"
     ]
    }
   ],
   "source": [
    "from provenanceDB import *"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## muon_reconstruction definition"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "\"\"\"\n",
    "Example to load raw data (hessio format), calibrate and reconstruct muon\n",
    "ring parameters, and write the muon ring and intensity parameters to an output\n",
    "table.\n",
    "\n",
    "The resulting output can be read e.g. using `pandas.read_hdf(filename,\n",
    "'muons/LSTCam')`\n",
    "\"\"\"\n",
    "\n",
    "import warnings\n",
    "from collections import defaultdict\n",
    "\n",
    "from tqdm import tqdm\n",
    "\n",
    "from ctapipe.calib import CameraCalibrator\n",
    "from ctapipe.core import Provenance\n",
    "from ctapipe.core import Tool, ToolConfigurationError\n",
    "from ctapipe.core import traits as t\n",
    "from ctapipe.image.muon.muon_diagnostic_plots import plot_muon_event\n",
    "from ctapipe.image.muon.muon_reco_functions import analyze_muon_event\n",
    "from ctapipe.io import EventSource, event_source\n",
    "from ctapipe.io import HDF5TableWriter\n",
    "\n",
    "warnings.filterwarnings(\"ignore\")  # Supresses iminuit warnings\n",
    "\n",
    "\n",
    "def _exclude_some_columns(subarray, writer):\n",
    "    \"\"\" a hack to exclude some columns of all output tables here we exclude\n",
    "    the prediction and mask quantities, since they are arrays and thus not\n",
    "    readable by pandas.  Also, prediction currently is a variable-length\n",
    "    quantity (need to change it to be fixed-length), so it cannot be written\n",
    "    to a fixed-length table.\n",
    "    \"\"\"\n",
    "    all_camids = {str(x.camera) for x in subarray.tel.values()}\n",
    "    for cam in all_camids:\n",
    "        writer.exclude(cam, 'prediction')\n",
    "        writer.exclude(cam, 'mask')\n",
    "\n",
    "class MuonDisplayerTool(Tool):\n",
    "    name = 'ctapipe-reconstruct-muons'\n",
    "    description = t.Unicode(__doc__)\n",
    "\n",
    "    events = t.Unicode(\"\",\n",
    "                       help=\"input event data file\").tag(config=True)\n",
    "\n",
    "    outfile = t.Unicode(\"muons.hdf5\", help='HDF5 output file name').tag(\n",
    "        config=True)\n",
    "\n",
    "    display = t.Bool(\n",
    "        help='display the camera events', default=False\n",
    "    ).tag(config=True)\n",
    "\n",
    "    classes = t.List([\n",
    "        CameraCalibrator, EventSource\n",
    "    ])\n",
    "\n",
    "    aliases = t.Dict({\n",
    "        'input': 'MuonDisplayerTool.events',\n",
    "        'outfile': 'MuonDisplayerTool.outfile',\n",
    "        'display': 'MuonDisplayerTool.display',\n",
    "        'max_events': 'EventSource.max_events',\n",
    "        'allowed_tels': 'EventSource.allowed_tels',\n",
    "    })\n",
    "\n",
    "    def setup(self):\n",
    "        if self.events == '':\n",
    "            raise ToolConfigurationError(\"please specify --input <events file>\")\n",
    "        self.log.debug(\"input: %s\", self.events)\n",
    "        self.source = event_source(self.events)\n",
    "        self.calib = CameraCalibrator(parent=self)\n",
    "        self.writer = HDF5TableWriter(self.outfile, \"muons\")\n",
    "\n",
    "    def start(self):\n",
    "\n",
    "        numev = 0\n",
    "        self.num_muons_found = defaultdict(int)\n",
    "\n",
    "        for event in tqdm(self.source, desc='detecting muons'):\n",
    "\n",
    "            self.calib(event)\n",
    "            muon_evt = analyze_muon_event(event)\n",
    "\n",
    "            if numev == 0:\n",
    "                _exclude_some_columns(event.inst.subarray, self.writer)\n",
    "\n",
    "            numev += 1\n",
    "\n",
    "            if not muon_evt['MuonIntensityParams']:\n",
    "                # No telescopes  contained a good muon\n",
    "                continue\n",
    "            else:\n",
    "                if self.display:\n",
    "                    plot_muon_event(event, muon_evt)\n",
    "\n",
    "                for tel_id in muon_evt['TelIds']:\n",
    "                    idx = muon_evt['TelIds'].index(tel_id)\n",
    "                    intens_params = muon_evt['MuonIntensityParams'][idx]\n",
    "\n",
    "                    if intens_params is not None:\n",
    "                        ring_params = muon_evt['MuonRingParams'][idx]\n",
    "                        cam_id = str(event.inst.subarray.tel[tel_id].camera)\n",
    "                        self.num_muons_found[cam_id] += 1\n",
    "                        self.log.debug(\"INTENSITY: %s\", intens_params)\n",
    "                        self.log.debug(\"RING: %s\", ring_params)\n",
    "                        self.writer.write(table_name=cam_id,\n",
    "                                          containers=[intens_params,\n",
    "                                                      ring_params])\n",
    "\n",
    "                self.log.info(\n",
    "                    \"Event Number: %d, found %s muons\",\n",
    "                    numev, dict(self.num_muons_found)\n",
    "                )\n",
    "\n",
    "    def finish(self):\n",
    "        Provenance().add_output_file(self.outfile,\n",
    "                                     role='dl1.tel.evt.muon')\n",
    "        self.writer.close()\n",
    "\n",
    "\n",
    "\n",
    "\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Descriptions added in the Provenance database"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-07-30 11:03:59,309 INFO sqlalchemy.engine.base.Engine BEGIN (implicit)\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "INFO:sqlalchemy.engine.base.Engine:BEGIN (implicit)\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-07-30 11:03:59,311 INFO sqlalchemy.engine.base.Engine INSERT INTO \"activityDescriptions\" (id, name, version, description, type, subtype, doculink) VALUES (?, ?, ?, ?, ?, ?, ?)\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "INFO:sqlalchemy.engine.base.Engine:INSERT INTO \"activityDescriptions\" (id, name, version, description, type, subtype, doculink) VALUES (?, ?, ?, ?, ?, ?, ?)\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-07-30 11:03:59,312 INFO sqlalchemy.engine.base.Engine ('ctapipe_display_muons_0.6.1', 'ctapipe_display_muons', '0.6.1', None, 'reconstruction', '', '')\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "INFO:sqlalchemy.engine.base.Engine:('ctapipe_display_muons_0.6.1', 'ctapipe_display_muons', '0.6.1', None, 'reconstruction', '', '')\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-07-30 11:03:59,324 INFO sqlalchemy.engine.base.Engine INSERT INTO \"entityDescriptions\" (id, name, type, description, doculink, \"classType\") VALUES (?, ?, ?, ?, ?, ?)\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "INFO:sqlalchemy.engine.base.Engine:INSERT INTO \"entityDescriptions\" (id, name, type, description, doculink, \"classType\") VALUES (?, ?, ?, ?, ?, ?)\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-07-30 11:03:59,326 INFO sqlalchemy.engine.base.Engine (('proton_events', 'protons', None, 'proton file', None, 'datasetDescription'), ('muons_hdf5', 'muons', None, 'muon file', None, 'datasetDescription'), ('status', None, None, None, None, 'valueDescription'))\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "INFO:sqlalchemy.engine.base.Engine:(('proton_events', 'protons', None, 'proton file', None, 'datasetDescription'), ('muons_hdf5', 'muons', None, 'muon file', None, 'datasetDescription'), ('status', None, None, None, None, 'valueDescription'))\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-07-30 11:03:59,331 INFO sqlalchemy.engine.base.Engine INSERT INTO \"valueDescriptions\" (id, \"valueType\", unit, ucd, utype, min, max, \"default\", options) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "INFO:sqlalchemy.engine.base.Engine:INSERT INTO \"valueDescriptions\" (id, \"valueType\", unit, ucd, utype, min, max, \"default\", options) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-07-30 11:03:59,334 INFO sqlalchemy.engine.base.Engine ('status', None, None, None, None, None, None, None, None)\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "INFO:sqlalchemy.engine.base.Engine:('status', None, None, None, None, None, None, None, None)\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-07-30 11:03:59,337 INFO sqlalchemy.engine.base.Engine INSERT INTO \"datasetDescriptions\" (id, \"contentType\") VALUES (?, ?)\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "INFO:sqlalchemy.engine.base.Engine:INSERT INTO \"datasetDescriptions\" (id, \"contentType\") VALUES (?, ?)\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-07-30 11:03:59,338 INFO sqlalchemy.engine.base.Engine (('proton_events', None), ('muons_hdf5', None))\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "INFO:sqlalchemy.engine.base.Engine:(('proton_events', None), ('muons_hdf5', None))\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-07-30 11:03:59,341 INFO sqlalchemy.engine.base.Engine INSERT INTO \"generationDescriptions\" (id, role, description, type, multiplicity, \"activityDescription_id\", \"entityDescription_id\") VALUES (?, ?, ?, ?, ?, ?, ?)\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "INFO:sqlalchemy.engine.base.Engine:INSERT INTO \"generationDescriptions\" (id, role, description, type, multiplicity, \"activityDescription_id\", \"entityDescription_id\") VALUES (?, ?, ?, ?, ?, ?, ?)\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-07-30 11:03:59,342 INFO sqlalchemy.engine.base.Engine (('ctapipe_display_muons_0.6.1_muons_hdf5', 'dl0.sub.evt', None, None, None, 'ctapipe_display_muons_0.6.1', 'muons_hdf5'), ('ctapipe_display_muons_0.6.1_status', 'quality', None, None, None, 'ctapipe_display_muons_0.6.1', 'status'))\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "INFO:sqlalchemy.engine.base.Engine:(('ctapipe_display_muons_0.6.1_muons_hdf5', 'dl0.sub.evt', None, None, None, 'ctapipe_display_muons_0.6.1', 'muons_hdf5'), ('ctapipe_display_muons_0.6.1_status', 'quality', None, None, None, 'ctapipe_display_muons_0.6.1', 'status'))\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-07-30 11:03:59,346 INFO sqlalchemy.engine.base.Engine INSERT INTO \"usageDescriptions\" (id, role, description, type, multiplicity, \"activityDescription_id\", \"entityDescription_id\") VALUES (?, ?, ?, ?, ?, ?, ?)\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "INFO:sqlalchemy.engine.base.Engine:INSERT INTO \"usageDescriptions\" (id, role, description, type, multiplicity, \"activityDescription_id\", \"entityDescription_id\") VALUES (?, ?, ?, ?, ?, ?, ?)\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-07-30 11:03:59,349 INFO sqlalchemy.engine.base.Engine ('ctapipe_display_muons_0.6.1_proton_events', 'dl0.sub.evt', None, None, None, 'ctapipe_display_muons_0.6.1', 'proton_events')\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "INFO:sqlalchemy.engine.base.Engine:('ctapipe_display_muons_0.6.1_proton_events', 'dl0.sub.evt', None, None, None, 'ctapipe_display_muons_0.6.1', 'proton_events')\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-07-30 11:03:59,351 INFO sqlalchemy.engine.base.Engine COMMIT\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "INFO:sqlalchemy.engine.base.Engine:COMMIT\n"
     ]
    }
   ],
   "source": [
    "# Define the session to talk to the database\n",
    "from sqlalchemy.orm import sessionmaker\n",
    "Session = sessionmaker(bind=engine)\n",
    "session = Session()\n",
    "\n",
    "# Create an instance of ActivityDescription \n",
    "actDesc1 = ActivityDescription(id='ctapipe_display_muons_0.6.1',name='ctapipe_display_muons',\\\n",
    "                               type='reconstruction',subtype='',version='0.6.1', doculink='')\n",
    "\n",
    "# Create the description of input entities\n",
    "dataDesc1 = DatasetDescription(id='proton_events', name='protons', description='proton file', classType='datasetDescription')\n",
    "usedDesc1 = UsageDescription(id='ctapipe_display_muons_0.6.1_proton_events',activityDescription=actDesc1, entityDescription=dataDesc1, role=\"dl0.sub.evt\")\n",
    "# Create the description of output entities\n",
    "dataDesc2  = DatasetDescription(id='muons_hdf5', name='muons', description='muon file', classType='datasetDescription')\n",
    "wGBDesc1   = GenerationDescription(id='ctapipe_display_muons_0.6.1_muons_hdf5',activityDescription=actDesc1, entityDescription=dataDesc2, role=\"dl0.sub.evt\")\n",
    "valueDesc1 = ValueDescription(id='status', classType='valueDescription')\n",
    "wGBDesc2   = GenerationDescription(id='ctapipe_display_muons_0.6.1_status', activityDescription=actDesc1, entityDescription=valueDesc1, role=\"quality\")\n",
    "\n",
    "# Put the instance in the database\n",
    "session.add(actDesc1)\n",
    "session.add(dataDesc1)\n",
    "session.add(usedDesc1)\n",
    "session.add(dataDesc2)\n",
    "session.add(wGBDesc1)\n",
    "session.add(valueDesc1)\n",
    "session.add(wGBDesc2)\n",
    "session.commit()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Run muon_reconstruction"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "\u001b[1;32mINFO\u001b[0m [MuonDisplayerTool] (tool/initialize): ctapipe version 0.6.2.post150+gita494195\n",
      "\u001b[1;32mINFO\u001b[0m [MuonDisplayerTool] (tool/run): Starting: ctapipe-reconstruct-muons\n"
     ]
    },
    {
     "ename": "TypeError",
     "evalue": "__init__() got an unexpected keyword argument 'zcat'",
     "output_type": "error",
     "traceback": [
      "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[0;31mTypeError\u001b[0m                                 Traceback (most recent call last)",
      "\u001b[0;32m<ipython-input-4-4d52e262ad14>\u001b[0m in \u001b[0;36m<module>\u001b[0;34m\u001b[0m\n\u001b[1;32m      7\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      8\u001b[0m \u001b[0mmyTool\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mMuonDisplayerTool\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m----> 9\u001b[0;31m \u001b[0mmyTool\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mrun\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m[\u001b[0m\u001b[0;34m'--input=proton_20deg_180deg_run22___cta-prod3-demo-2147m-LaPalma-baseline.simtel.gz'\u001b[0m\u001b[0;34m]\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m     10\u001b[0m \u001b[0;31m#print(myTool.get_current_config())\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     11\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;32m~/Documents/CTA/Provenance/ctasoft/ctapipe/ctapipe/core/tool.py\u001b[0m in \u001b[0;36mrun\u001b[0;34m(self, argv)\u001b[0m\n\u001b[1;32m    163\u001b[0m             \u001b[0mProvenance\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mstart_activity\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mname\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    164\u001b[0m             \u001b[0mProvenance\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0madd_config\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mconfig\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 165\u001b[0;31m             \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0msetup\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    166\u001b[0m             \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mis_setup\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0;32mTrue\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    167\u001b[0m             \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mstart\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;32m<ipython-input-2-8a4429e1aa3b>\u001b[0m in \u001b[0;36msetup\u001b[0;34m(self)\u001b[0m\n\u001b[1;32m     67\u001b[0m             \u001b[0;32mraise\u001b[0m \u001b[0mToolConfigurationError\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m\"please specify --input <events file>\"\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     68\u001b[0m         \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mlog\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mdebug\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m\"input: %s\"\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mevents\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m---> 69\u001b[0;31m         \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0msource\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mevent_source\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mevents\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m     70\u001b[0m         \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mcalib\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mCameraCalibrator\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mparent\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mself\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     71\u001b[0m         \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mwriter\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mHDF5TableWriter\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0moutfile\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0;34m\"muons\"\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;32m~/Documents/CTA/Provenance/ctasoft/ctapipe/ctapipe/io/eventsource.py\u001b[0m in \u001b[0;36mevent_source\u001b[0;34m(input_url, **kwargs)\u001b[0m\n\u001b[1;32m     35\u001b[0m         \u001b[0mInstance\u001b[0m \u001b[0mof\u001b[0m \u001b[0ma\u001b[0m \u001b[0mcompatible\u001b[0m \u001b[0mEventSource\u001b[0m \u001b[0msubclass\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     36\u001b[0m     \"\"\"\n\u001b[0;32m---> 37\u001b[0;31m     \u001b[0;32mreturn\u001b[0m \u001b[0mEventSource\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mfrom_url\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0minput_url\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0;34m**\u001b[0m\u001b[0mkwargs\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m     38\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     39\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;32m~/Documents/CTA/Provenance/ctasoft/ctapipe/ctapipe/io/eventsource.py\u001b[0m in \u001b[0;36mfrom_url\u001b[0;34m(cls, input_url, **kwargs)\u001b[0m\n\u001b[1;32m    247\u001b[0m         \u001b[0;32mfor\u001b[0m \u001b[0msubcls\u001b[0m \u001b[0;32min\u001b[0m \u001b[0mavailable_classes\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    248\u001b[0m             \u001b[0;32mif\u001b[0m \u001b[0msubcls\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mis_compatible\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0minput_url\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 249\u001b[0;31m                 \u001b[0;32mreturn\u001b[0m \u001b[0msubcls\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0minput_url\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0minput_url\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0;34m**\u001b[0m\u001b[0mkwargs\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    250\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    251\u001b[0m         raise ValueError(\n",
      "\u001b[0;32m~/Documents/CTA/Provenance/ctasoft/ctapipe/ctapipe/io/simteleventsource.py\u001b[0m in \u001b[0;36m__init__\u001b[0;34m(self, config, parent, **kwargs)\u001b[0m\n\u001b[1;32m     76\u001b[0m             \u001b[0mallowed_telescopes\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mallowed_tels\u001b[0m \u001b[0;32mif\u001b[0m \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mallowed_tels\u001b[0m \u001b[0;32melse\u001b[0m \u001b[0;32mNone\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     77\u001b[0m             \u001b[0mskip_calibration\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mskip_calibration_events\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m---> 78\u001b[0;31m             \u001b[0mzcat\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0;32mnot\u001b[0m \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mback_seekable\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m     79\u001b[0m         )\n\u001b[1;32m     80\u001b[0m         \u001b[0;32mif\u001b[0m \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mback_seekable\u001b[0m \u001b[0;32mand\u001b[0m \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mis_stream\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;31mTypeError\u001b[0m: __init__() got an unexpected keyword argument 'zcat'"
     ]
    }
   ],
   "source": [
    "from ctapipe.core import Provenance\n",
    "from pprint import pprint\n",
    "p = Provenance()  # note this is a singleton, so only ever one global provenence object\n",
    "p.clear()\n",
    "\n",
    "p.start_activity()\n",
    "    \n",
    "myTool = MuonDisplayerTool()\n",
    "myTool.run(['--input=proton_20deg_180deg_run22___cta-prod3-demo-2147m-LaPalma-baseline.simtel.gz'])\n",
    "#print(myTool.get_current_config())\n",
    "\n",
    "#myTool = MuonDisplayerTool()\n",
    "#myTool.run(['--input=proton_20deg_180deg_run22___cta-prod3-demo-2147m-LaPalma-baseline.simtel.gz'])\n",
    "\n",
    "p.finish_activity()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "[]"
      ]
     },
     "execution_count": 5,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "p.finished_activity_names"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "[]"
      ]
     },
     "execution_count": 6,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "p.provenance[:-1]"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Provenance database update"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-07-30 11:06:20,451 INFO sqlalchemy.engine.base.Engine BEGIN (implicit)\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "INFO:sqlalchemy.engine.base.Engine:BEGIN (implicit)\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-07-30 11:06:20,455 INFO sqlalchemy.engine.base.Engine INSERT INTO agents (id, name, type, email, affiliation, phone, address, comment, url) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "INFO:sqlalchemy.engine.base.Engine:INSERT INTO agents (id, name, type, email, affiliation, phone, address, comment, url) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-07-30 11:06:20,456 INFO sqlalchemy.engine.base.Engine ('CTAO', 'CTA Observatory', 'Organization', None, None, None, None, None, None)\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "INFO:sqlalchemy.engine.base.Engine:('CTAO', 'CTA Observatory', 'Organization', None, None, None, None, None, None)\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-07-30 11:06:20,459 INFO sqlalchemy.engine.base.Engine COMMIT\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "INFO:sqlalchemy.engine.base.Engine:COMMIT\n"
     ]
    }
   ],
   "source": [
    "import hashlib, uuid, os\n",
    "BLOCKSIZE = 65536\n",
    "hasher = hashlib.sha1()\n",
    "\n",
    "def get_file_id(url):\n",
    "    '''\n",
    "    # Computation of the hash of the file to determine the id of it\n",
    "    with open(cta_input['url'], 'rb') as afile:\n",
    "        buf = afile.read(BLOCKSIZE)\n",
    "        while len(buf) > 0:\n",
    "            hasher.update(buf)\n",
    "            buf = afile.read(BLOCKSIZE)\n",
    "            return hasher.hexdigest()\n",
    "    '''\n",
    "    logical_name = url.split('/')[-1] \n",
    "    name = logical_name + str(os.path.getctime(url))\n",
    "    file_uuid = uuid.uuid5(uuid.NAMESPACE_URL, name)\n",
    "    if session.query(exists().where(DatasetEntity.id==file_uuid)):\n",
    "        print (\"cle existante : \", logical_name)\n",
    "        return str(file_uuid)\n",
    "    else:\n",
    "        print (\"cle non existante : \", logical_name)\n",
    "        return \"\"\n",
    "\n",
    "    # universal unique id\n",
    "    #return uuid.uuid4()\n",
    "\n",
    "def set_file_id(url):\n",
    "    logical_name = url.split('/')[-1] \n",
    "    name = logical_name + str(os.path.getctime(url))\n",
    "    file_uuid = uuid.uuid5(uuid.NAMESPACE_URL, name)\n",
    "    return str(file_uuid)\n",
    "\n",
    "def add_activity(session, cta_activity):\n",
    "    #print(\"XxxxxxxXXXXXXXX\", (session.query(exists().where(Activity.id==cta_activity['activity_uuid'])))\n",
    "    #if not session.query(exists().where(Activity.id==cta_activity['activity_uuid'])): # for the tests\n",
    "    if True:\n",
    "        current_activity = Activity(id=cta_activity['activity_uuid'])\n",
    "        current_activity.name=cta_activity['activity_name']\n",
    "        current_activity.startTime=cta_activity['start']['time_utc']\n",
    "        current_activity.endTime=cta_activity['stop']['time_utc']\n",
    "        current_activity.comment=''\n",
    "        current_activity.activityDescription_id=cta_activity['activity_name']+'_'+cta_activity['system']['ctapipe_version']\n",
    "        session.add(current_activity)\n",
    "    \n",
    "        # Association with the agent\n",
    "        wAW = WasAssociatedWith()\n",
    "        wAW.activity = cta_activity['activity_uuid']\n",
    "        wAW.agent    = \"CTAO\"\n",
    "        #wAW.role = ?\n",
    "        session.add(wAW)\n",
    "    \n",
    "\n",
    "# CTAO Agent\n",
    "agent = Agent(id=\"CTAO\")\n",
    "agent.name =\"CTA Observatory\"\n",
    "agent.type = \"Organization\"\n",
    "session.add(agent)\n",
    "\n",
    "# For each activity\n",
    "for cta_activity in p.provenance[:-1]:\n",
    "    add_activity(session, cta_activity)\n",
    "    \n",
    "    # For each input file\n",
    "    for cta_input in cta_activity['input']:\n",
    "        \n",
    "        # Get the id of the file\n",
    "        filename_uuid = get_file_id(cta_input['url'])\n",
    "            \n",
    "        # If Entity does not exist in the database, add it - current_input_file.entityDescription_id= ???\n",
    "        #if filename_uuid == \"\":\n",
    "        if True:\n",
    "            current_input_file = DatasetEntity(id=filename_uuid, classType = 'dataset', \\\n",
    "                                    name = cta_input['url'].split('/')[-1], location = cta_input['url'])\n",
    "            session.add(current_input_file)\n",
    "            \n",
    "            # Attribution to the agent - wAT.role = ?\n",
    "            wAT = WasAttributedTo(entity = filename_uuid, agent = \"CTAO\")\n",
    "            session.add(wAT)\n",
    "            \n",
    "        # Add the Used relationship\n",
    "        used1 = Used(role = cta_input['role'], activity_id = cta_activity['activity_uuid'], entity_id = filename_uuid) # incremental id\n",
    "        session.add(used1)\n",
    "    \n",
    "    # For each output file\n",
    "    for cta_output in cta_activity['output']:\n",
    "        \n",
    "        # Computation of the hash of the file to determine the id of it\n",
    "        filename_uuid = set_file_id(cta_output['url'])\n",
    "            \n",
    "        # If Entity already exists in the database, raise an Exception or a error message - #current_output_file.entityDescription_id= ???\n",
    "        #if session.query(exists().where(DatasetEntity.id==filename_uuid)):\n",
    "            #print (\"ERROR\")\n",
    "        #else:\n",
    "        if True:\n",
    "            current_output_file = DatasetEntity(id=filename_uuid, classType = 'dataset', name = cta_output['url'].split('/')[-1],\\\n",
    "                                               location = cta_output['url'])\n",
    "            session.add(current_output_file)\n",
    "            \n",
    "            # Attribution to the agent - wAT.role = ?\n",
    "            wAT = WasAttributedTo(entity = filename_uuid, agent = \"CTAO\")\n",
    "            session.add(wAT)\n",
    "            \n",
    "        # Add the wasgeneratedBy relationship - incremental id\n",
    "        wGB1 = WasGeneratedBy(role = cta_output['role'], activity_id = cta_activity['activity_uuid'],\\\n",
    "                             entity_id = filename_uuid) \n",
    "        session.add(wGB1)\n",
    "        \n",
    "    # Add the status as an output ValueEntity\n",
    "    current_output_value = ValueEntity(id=cta_activity['activity_uuid']+'_status')\n",
    "    current_output_value.name = 'status'\n",
    "    current_output_value.classType = 'value'\n",
    "    current_output_value.valueXX = cta_activity['status']\n",
    "    current_output_value.entityDescription_id = 'status'\n",
    "    #current_output_value.location\n",
    "    #current_output_value.entityDescription_id= ???\n",
    "    session.add(current_output_value)\n",
    "    \n",
    "    # Add the wasgeneratedBy relationship - incremental id\n",
    "    wGB2 = WasGeneratedBy(role = 'status', activity_id = cta_activity['activity_uuid'],\\\n",
    "                             entity_id = cta_activity['activity_uuid']+'_status') \n",
    "    session.add(wGB2)\n",
    "        \n",
    "session.commit()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Store the items of the database in a file"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-07-30 11:06:55,949 INFO sqlalchemy.engine.base.Engine BEGIN (implicit)\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "INFO:sqlalchemy.engine.base.Engine:BEGIN (implicit)\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-07-30 11:06:55,952 INFO sqlalchemy.engine.base.Engine SELECT \"activityDescriptions\".id AS \"activityDescriptions_id\", \"activityDescriptions\".name AS \"activityDescriptions_name\", \"activityDescriptions\".version AS \"activityDescriptions_version\", \"activityDescriptions\".description AS \"activityDescriptions_description\", \"activityDescriptions\".type AS \"activityDescriptions_type\", \"activityDescriptions\".subtype AS \"activityDescriptions_subtype\", \"activityDescriptions\".doculink AS \"activityDescriptions_doculink\" \n",
      "FROM \"activityDescriptions\" ORDER BY \"activityDescriptions\".id\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "INFO:sqlalchemy.engine.base.Engine:SELECT \"activityDescriptions\".id AS \"activityDescriptions_id\", \"activityDescriptions\".name AS \"activityDescriptions_name\", \"activityDescriptions\".version AS \"activityDescriptions_version\", \"activityDescriptions\".description AS \"activityDescriptions_description\", \"activityDescriptions\".type AS \"activityDescriptions_type\", \"activityDescriptions\".subtype AS \"activityDescriptions_subtype\", \"activityDescriptions\".doculink AS \"activityDescriptions_doculink\" \n",
      "FROM \"activityDescriptions\" ORDER BY \"activityDescriptions\".id\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-07-30 11:06:55,954 INFO sqlalchemy.engine.base.Engine ()\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "INFO:sqlalchemy.engine.base.Engine:()\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-07-30 11:06:55,956 INFO sqlalchemy.engine.base.Engine SELECT \"entityDescriptions\".id AS \"entityDescriptions_id\", \"entityDescriptions\".name AS \"entityDescriptions_name\", \"entityDescriptions\".type AS \"entityDescriptions_type\", \"entityDescriptions\".description AS \"entityDescriptions_description\", \"entityDescriptions\".doculink AS \"entityDescriptions_doculink\", \"entityDescriptions\".\"classType\" AS \"entityDescriptions_classType\" \n",
      "FROM \"entityDescriptions\" ORDER BY \"entityDescriptions\".id\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "INFO:sqlalchemy.engine.base.Engine:SELECT \"entityDescriptions\".id AS \"entityDescriptions_id\", \"entityDescriptions\".name AS \"entityDescriptions_name\", \"entityDescriptions\".type AS \"entityDescriptions_type\", \"entityDescriptions\".description AS \"entityDescriptions_description\", \"entityDescriptions\".doculink AS \"entityDescriptions_doculink\", \"entityDescriptions\".\"classType\" AS \"entityDescriptions_classType\" \n",
      "FROM \"entityDescriptions\" ORDER BY \"entityDescriptions\".id\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-07-30 11:06:55,958 INFO sqlalchemy.engine.base.Engine ()\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "INFO:sqlalchemy.engine.base.Engine:()\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-07-30 11:06:55,962 INFO sqlalchemy.engine.base.Engine SELECT \"usageDescriptions\".id AS \"usageDescriptions_id\", \"usageDescriptions\".role AS \"usageDescriptions_role\", \"usageDescriptions\".description AS \"usageDescriptions_description\", \"usageDescriptions\".type AS \"usageDescriptions_type\", \"usageDescriptions\".multiplicity AS \"usageDescriptions_multiplicity\", \"usageDescriptions\".\"activityDescription_id\" AS \"usageDescriptions_activityDescription_id\", \"usageDescriptions\".\"entityDescription_id\" AS \"usageDescriptions_entityDescription_id\" \n",
      "FROM \"usageDescriptions\" ORDER BY \"usageDescriptions\".id\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "INFO:sqlalchemy.engine.base.Engine:SELECT \"usageDescriptions\".id AS \"usageDescriptions_id\", \"usageDescriptions\".role AS \"usageDescriptions_role\", \"usageDescriptions\".description AS \"usageDescriptions_description\", \"usageDescriptions\".type AS \"usageDescriptions_type\", \"usageDescriptions\".multiplicity AS \"usageDescriptions_multiplicity\", \"usageDescriptions\".\"activityDescription_id\" AS \"usageDescriptions_activityDescription_id\", \"usageDescriptions\".\"entityDescription_id\" AS \"usageDescriptions_entityDescription_id\" \n",
      "FROM \"usageDescriptions\" ORDER BY \"usageDescriptions\".id\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-07-30 11:06:55,963 INFO sqlalchemy.engine.base.Engine ()\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "INFO:sqlalchemy.engine.base.Engine:()\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-07-30 11:06:55,966 INFO sqlalchemy.engine.base.Engine SELECT \"generationDescriptions\".id AS \"generationDescriptions_id\", \"generationDescriptions\".role AS \"generationDescriptions_role\", \"generationDescriptions\".description AS \"generationDescriptions_description\", \"generationDescriptions\".type AS \"generationDescriptions_type\", \"generationDescriptions\".multiplicity AS \"generationDescriptions_multiplicity\", \"generationDescriptions\".\"activityDescription_id\" AS \"generationDescriptions_activityDescription_id\", \"generationDescriptions\".\"entityDescription_id\" AS \"generationDescriptions_entityDescription_id\" \n",
      "FROM \"generationDescriptions\" ORDER BY \"generationDescriptions\".id\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "INFO:sqlalchemy.engine.base.Engine:SELECT \"generationDescriptions\".id AS \"generationDescriptions_id\", \"generationDescriptions\".role AS \"generationDescriptions_role\", \"generationDescriptions\".description AS \"generationDescriptions_description\", \"generationDescriptions\".type AS \"generationDescriptions_type\", \"generationDescriptions\".multiplicity AS \"generationDescriptions_multiplicity\", \"generationDescriptions\".\"activityDescription_id\" AS \"generationDescriptions_activityDescription_id\", \"generationDescriptions\".\"entityDescription_id\" AS \"generationDescriptions_entityDescription_id\" \n",
      "FROM \"generationDescriptions\" ORDER BY \"generationDescriptions\".id\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-07-30 11:06:55,967 INFO sqlalchemy.engine.base.Engine ()\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "INFO:sqlalchemy.engine.base.Engine:()\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-07-30 11:06:55,970 INFO sqlalchemy.engine.base.Engine SELECT \"datasetDescriptions\".id AS \"datasetDescriptions_id\", \"entityDescriptions\".id AS \"entityDescriptions_id\", \"entityDescriptions\".name AS \"entityDescriptions_name\", \"entityDescriptions\".type AS \"entityDescriptions_type\", \"entityDescriptions\".description AS \"entityDescriptions_description\", \"entityDescriptions\".doculink AS \"entityDescriptions_doculink\", \"entityDescriptions\".\"classType\" AS \"entityDescriptions_classType\", \"datasetDescriptions\".\"contentType\" AS \"datasetDescriptions_contentType\" \n",
      "FROM \"entityDescriptions\" JOIN \"datasetDescriptions\" ON \"entityDescriptions\".id = \"datasetDescriptions\".id ORDER BY \"datasetDescriptions\".id\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "INFO:sqlalchemy.engine.base.Engine:SELECT \"datasetDescriptions\".id AS \"datasetDescriptions_id\", \"entityDescriptions\".id AS \"entityDescriptions_id\", \"entityDescriptions\".name AS \"entityDescriptions_name\", \"entityDescriptions\".type AS \"entityDescriptions_type\", \"entityDescriptions\".description AS \"entityDescriptions_description\", \"entityDescriptions\".doculink AS \"entityDescriptions_doculink\", \"entityDescriptions\".\"classType\" AS \"entityDescriptions_classType\", \"datasetDescriptions\".\"contentType\" AS \"datasetDescriptions_contentType\" \n",
      "FROM \"entityDescriptions\" JOIN \"datasetDescriptions\" ON \"entityDescriptions\".id = \"datasetDescriptions\".id ORDER BY \"datasetDescriptions\".id\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-07-30 11:06:55,972 INFO sqlalchemy.engine.base.Engine ()\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "INFO:sqlalchemy.engine.base.Engine:()\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-07-30 11:06:55,978 INFO sqlalchemy.engine.base.Engine SELECT \"valueDescriptions\".id AS \"valueDescriptions_id\", \"entityDescriptions\".id AS \"entityDescriptions_id\", \"entityDescriptions\".name AS \"entityDescriptions_name\", \"entityDescriptions\".type AS \"entityDescriptions_type\", \"entityDescriptions\".description AS \"entityDescriptions_description\", \"entityDescriptions\".doculink AS \"entityDescriptions_doculink\", \"entityDescriptions\".\"classType\" AS \"entityDescriptions_classType\", \"valueDescriptions\".\"valueType\" AS \"valueDescriptions_valueType\", \"valueDescriptions\".unit AS \"valueDescriptions_unit\", \"valueDescriptions\".ucd AS \"valueDescriptions_ucd\", \"valueDescriptions\".utype AS \"valueDescriptions_utype\", \"valueDescriptions\".min AS \"valueDescriptions_min\", \"valueDescriptions\".max AS \"valueDescriptions_max\", \"valueDescriptions\".\"default\" AS \"valueDescriptions_default\", \"valueDescriptions\".options AS \"valueDescriptions_options\" \n",
      "FROM \"entityDescriptions\" JOIN \"valueDescriptions\" ON \"entityDescriptions\".id = \"valueDescriptions\".id ORDER BY \"valueDescriptions\".id\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "INFO:sqlalchemy.engine.base.Engine:SELECT \"valueDescriptions\".id AS \"valueDescriptions_id\", \"entityDescriptions\".id AS \"entityDescriptions_id\", \"entityDescriptions\".name AS \"entityDescriptions_name\", \"entityDescriptions\".type AS \"entityDescriptions_type\", \"entityDescriptions\".description AS \"entityDescriptions_description\", \"entityDescriptions\".doculink AS \"entityDescriptions_doculink\", \"entityDescriptions\".\"classType\" AS \"entityDescriptions_classType\", \"valueDescriptions\".\"valueType\" AS \"valueDescriptions_valueType\", \"valueDescriptions\".unit AS \"valueDescriptions_unit\", \"valueDescriptions\".ucd AS \"valueDescriptions_ucd\", \"valueDescriptions\".utype AS \"valueDescriptions_utype\", \"valueDescriptions\".min AS \"valueDescriptions_min\", \"valueDescriptions\".max AS \"valueDescriptions_max\", \"valueDescriptions\".\"default\" AS \"valueDescriptions_default\", \"valueDescriptions\".options AS \"valueDescriptions_options\" \n",
      "FROM \"entityDescriptions\" JOIN \"valueDescriptions\" ON \"entityDescriptions\".id = \"valueDescriptions\".id ORDER BY \"valueDescriptions\".id\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-07-30 11:06:55,982 INFO sqlalchemy.engine.base.Engine ()\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "INFO:sqlalchemy.engine.base.Engine:()\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-07-30 11:06:55,986 INFO sqlalchemy.engine.base.Engine SELECT \"parameterDescriptions\".id AS \"parameterDescriptions_id\", \"parameterDescriptions\".name AS \"parameterDescriptions_name\", \"parameterDescriptions\".\"valueType\" AS \"parameterDescriptions_valueType\", \"parameterDescriptions\".unit AS \"parameterDescriptions_unit\", \"parameterDescriptions\".ucd AS \"parameterDescriptions_ucd\", \"parameterDescriptions\".utype AS \"parameterDescriptions_utype\", \"parameterDescriptions\".min AS \"parameterDescriptions_min\", \"parameterDescriptions\".max AS \"parameterDescriptions_max\", \"parameterDescriptions\".options AS \"parameterDescriptions_options\", \"parameterDescriptions\".\"default\" AS \"parameterDescriptions_default\", \"parameterDescriptions\".description AS \"parameterDescriptions_description\" \n",
      "FROM \"parameterDescriptions\" ORDER BY \"parameterDescriptions\".id\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "INFO:sqlalchemy.engine.base.Engine:SELECT \"parameterDescriptions\".id AS \"parameterDescriptions_id\", \"parameterDescriptions\".name AS \"parameterDescriptions_name\", \"parameterDescriptions\".\"valueType\" AS \"parameterDescriptions_valueType\", \"parameterDescriptions\".unit AS \"parameterDescriptions_unit\", \"parameterDescriptions\".ucd AS \"parameterDescriptions_ucd\", \"parameterDescriptions\".utype AS \"parameterDescriptions_utype\", \"parameterDescriptions\".min AS \"parameterDescriptions_min\", \"parameterDescriptions\".max AS \"parameterDescriptions_max\", \"parameterDescriptions\".options AS \"parameterDescriptions_options\", \"parameterDescriptions\".\"default\" AS \"parameterDescriptions_default\", \"parameterDescriptions\".description AS \"parameterDescriptions_description\" \n",
      "FROM \"parameterDescriptions\" ORDER BY \"parameterDescriptions\".id\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-07-30 11:06:55,987 INFO sqlalchemy.engine.base.Engine ()\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "INFO:sqlalchemy.engine.base.Engine:()\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-07-30 11:06:55,992 INFO sqlalchemy.engine.base.Engine SELECT activities.id AS activities_id, activities.name AS activities_name, activities.\"startTime\" AS \"activities_startTime\", activities.\"endTime\" AS \"activities_endTime\", activities.comment AS activities_comment, activities.\"activityDescription_id\" AS \"activities_activityDescription_id\" \n",
      "FROM activities ORDER BY activities.id\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "INFO:sqlalchemy.engine.base.Engine:SELECT activities.id AS activities_id, activities.name AS activities_name, activities.\"startTime\" AS \"activities_startTime\", activities.\"endTime\" AS \"activities_endTime\", activities.comment AS activities_comment, activities.\"activityDescription_id\" AS \"activities_activityDescription_id\" \n",
      "FROM activities ORDER BY activities.id\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-07-30 11:06:55,993 INFO sqlalchemy.engine.base.Engine ()\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "INFO:sqlalchemy.engine.base.Engine:()\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-07-30 11:06:56,001 INFO sqlalchemy.engine.base.Engine SELECT entities.id AS entities_id, entities.name AS entities_name, entities.location AS entities_location, entities.\"generatedAtTime\" AS \"entities_generatedAtTime\", entities.\"invalidatedAtTime\" AS \"entities_invalidatedAtTime\", entities.comment AS entities_comment, entities.\"entityDescription_id\" AS \"entities_entityDescription_id\", entities.\"classType\" AS \"entities_classType\" \n",
      "FROM entities ORDER BY entities.id\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "INFO:sqlalchemy.engine.base.Engine:SELECT entities.id AS entities_id, entities.name AS entities_name, entities.location AS entities_location, entities.\"generatedAtTime\" AS \"entities_generatedAtTime\", entities.\"invalidatedAtTime\" AS \"entities_invalidatedAtTime\", entities.comment AS entities_comment, entities.\"entityDescription_id\" AS \"entities_entityDescription_id\", entities.\"classType\" AS \"entities_classType\" \n",
      "FROM entities ORDER BY entities.id\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-07-30 11:06:56,004 INFO sqlalchemy.engine.base.Engine ()\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "INFO:sqlalchemy.engine.base.Engine:()\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-07-30 11:06:56,009 INFO sqlalchemy.engine.base.Engine SELECT used.id AS used_id, used.role AS used_role, used.time AS used_time, used.activity_id AS used_activity_id, used.entity_id AS used_entity_id, used.\"usageDescription_id\" AS \"used_usageDescription_id\" \n",
      "FROM used ORDER BY used.id\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "INFO:sqlalchemy.engine.base.Engine:SELECT used.id AS used_id, used.role AS used_role, used.time AS used_time, used.activity_id AS used_activity_id, used.entity_id AS used_entity_id, used.\"usageDescription_id\" AS \"used_usageDescription_id\" \n",
      "FROM used ORDER BY used.id\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-07-30 11:06:56,011 INFO sqlalchemy.engine.base.Engine ()\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "INFO:sqlalchemy.engine.base.Engine:()\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-07-30 11:06:56,016 INFO sqlalchemy.engine.base.Engine SELECT \"wasGeneratedBy\".id AS \"wasGeneratedBy_id\", \"wasGeneratedBy\".role AS \"wasGeneratedBy_role\", \"wasGeneratedBy\".activity_id AS \"wasGeneratedBy_activity_id\", \"wasGeneratedBy\".entity_id AS \"wasGeneratedBy_entity_id\", \"wasGeneratedBy\".\"generationDescription_id\" AS \"wasGeneratedBy_generationDescription_id\" \n",
      "FROM \"wasGeneratedBy\" ORDER BY \"wasGeneratedBy\".id\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "INFO:sqlalchemy.engine.base.Engine:SELECT \"wasGeneratedBy\".id AS \"wasGeneratedBy_id\", \"wasGeneratedBy\".role AS \"wasGeneratedBy_role\", \"wasGeneratedBy\".activity_id AS \"wasGeneratedBy_activity_id\", \"wasGeneratedBy\".entity_id AS \"wasGeneratedBy_entity_id\", \"wasGeneratedBy\".\"generationDescription_id\" AS \"wasGeneratedBy_generationDescription_id\" \n",
      "FROM \"wasGeneratedBy\" ORDER BY \"wasGeneratedBy\".id\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-07-30 11:06:56,017 INFO sqlalchemy.engine.base.Engine ()\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "INFO:sqlalchemy.engine.base.Engine:()\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-07-30 11:06:56,020 INFO sqlalchemy.engine.base.Engine SELECT \"datasetEntities\".id AS \"datasetEntities_id\", entities.id AS entities_id, entities.name AS entities_name, entities.location AS entities_location, entities.\"generatedAtTime\" AS \"entities_generatedAtTime\", entities.\"invalidatedAtTime\" AS \"entities_invalidatedAtTime\", entities.comment AS entities_comment, entities.\"entityDescription_id\" AS \"entities_entityDescription_id\", entities.\"classType\" AS \"entities_classType\" \n",
      "FROM entities JOIN \"datasetEntities\" ON entities.id = \"datasetEntities\".id ORDER BY \"datasetEntities\".id\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "INFO:sqlalchemy.engine.base.Engine:SELECT \"datasetEntities\".id AS \"datasetEntities_id\", entities.id AS entities_id, entities.name AS entities_name, entities.location AS entities_location, entities.\"generatedAtTime\" AS \"entities_generatedAtTime\", entities.\"invalidatedAtTime\" AS \"entities_invalidatedAtTime\", entities.comment AS entities_comment, entities.\"entityDescription_id\" AS \"entities_entityDescription_id\", entities.\"classType\" AS \"entities_classType\" \n",
      "FROM entities JOIN \"datasetEntities\" ON entities.id = \"datasetEntities\".id ORDER BY \"datasetEntities\".id\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-07-30 11:06:56,021 INFO sqlalchemy.engine.base.Engine ()\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "INFO:sqlalchemy.engine.base.Engine:()\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-07-30 11:06:56,024 INFO sqlalchemy.engine.base.Engine SELECT \"valueEntities\".id AS \"valueEntities_id\", entities.id AS entities_id, entities.name AS entities_name, entities.location AS entities_location, entities.\"generatedAtTime\" AS \"entities_generatedAtTime\", entities.\"invalidatedAtTime\" AS \"entities_invalidatedAtTime\", entities.comment AS entities_comment, entities.\"entityDescription_id\" AS \"entities_entityDescription_id\", entities.\"classType\" AS \"entities_classType\", \"valueEntities\".value AS \"valueEntities_value\" \n",
      "FROM entities JOIN \"valueEntities\" ON entities.id = \"valueEntities\".id ORDER BY \"valueEntities\".id\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "INFO:sqlalchemy.engine.base.Engine:SELECT \"valueEntities\".id AS \"valueEntities_id\", entities.id AS entities_id, entities.name AS entities_name, entities.location AS entities_location, entities.\"generatedAtTime\" AS \"entities_generatedAtTime\", entities.\"invalidatedAtTime\" AS \"entities_invalidatedAtTime\", entities.comment AS entities_comment, entities.\"entityDescription_id\" AS \"entities_entityDescription_id\", entities.\"classType\" AS \"entities_classType\", \"valueEntities\".value AS \"valueEntities_value\" \n",
      "FROM entities JOIN \"valueEntities\" ON entities.id = \"valueEntities\".id ORDER BY \"valueEntities\".id\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-07-30 11:06:56,025 INFO sqlalchemy.engine.base.Engine ()\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "INFO:sqlalchemy.engine.base.Engine:()\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-07-30 11:06:56,028 INFO sqlalchemy.engine.base.Engine SELECT parameters.id AS parameters_id, parameters.value AS parameters_value, parameters.name AS parameters_name, parameters.\"parameterDescription_id\" AS \"parameters_parameterDescription_id\" \n",
      "FROM parameters ORDER BY parameters.id\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "INFO:sqlalchemy.engine.base.Engine:SELECT parameters.id AS parameters_id, parameters.value AS parameters_value, parameters.name AS parameters_name, parameters.\"parameterDescription_id\" AS \"parameters_parameterDescription_id\" \n",
      "FROM parameters ORDER BY parameters.id\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-07-30 11:06:56,029 INFO sqlalchemy.engine.base.Engine ()\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "INFO:sqlalchemy.engine.base.Engine:()\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-07-30 11:06:56,032 INFO sqlalchemy.engine.base.Engine SELECT agents.id AS agents_id, agents.name AS agents_name, agents.type AS agents_type, agents.email AS agents_email, agents.affiliation AS agents_affiliation, agents.phone AS agents_phone, agents.address AS agents_address, agents.comment AS agents_comment, agents.url AS agents_url \n",
      "FROM agents ORDER BY agents.id\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "INFO:sqlalchemy.engine.base.Engine:SELECT agents.id AS agents_id, agents.name AS agents_name, agents.type AS agents_type, agents.email AS agents_email, agents.affiliation AS agents_affiliation, agents.phone AS agents_phone, agents.address AS agents_address, agents.comment AS agents_comment, agents.url AS agents_url \n",
      "FROM agents ORDER BY agents.id\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-07-30 11:06:56,033 INFO sqlalchemy.engine.base.Engine ()\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "INFO:sqlalchemy.engine.base.Engine:()\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-07-30 11:06:56,035 INFO sqlalchemy.engine.base.Engine SELECT \"wasAttributedTo\".id AS \"wasAttributedTo_id\", \"wasAttributedTo\".role AS \"wasAttributedTo_role\", \"wasAttributedTo\".entity AS \"wasAttributedTo_entity\", \"wasAttributedTo\".agent AS \"wasAttributedTo_agent\" \n",
      "FROM \"wasAttributedTo\" ORDER BY \"wasAttributedTo\".id\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "INFO:sqlalchemy.engine.base.Engine:SELECT \"wasAttributedTo\".id AS \"wasAttributedTo_id\", \"wasAttributedTo\".role AS \"wasAttributedTo_role\", \"wasAttributedTo\".entity AS \"wasAttributedTo_entity\", \"wasAttributedTo\".agent AS \"wasAttributedTo_agent\" \n",
      "FROM \"wasAttributedTo\" ORDER BY \"wasAttributedTo\".id\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-07-30 11:06:56,036 INFO sqlalchemy.engine.base.Engine ()\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "INFO:sqlalchemy.engine.base.Engine:()\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-07-30 11:06:56,039 INFO sqlalchemy.engine.base.Engine SELECT \"wasAssociatedWith\".id AS \"wasAssociatedWith_id\", \"wasAssociatedWith\".role AS \"wasAssociatedWith_role\", \"wasAssociatedWith\".activity AS \"wasAssociatedWith_activity\", \"wasAssociatedWith\".agent AS \"wasAssociatedWith_agent\" \n",
      "FROM \"wasAssociatedWith\" ORDER BY \"wasAssociatedWith\".id\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "INFO:sqlalchemy.engine.base.Engine:SELECT \"wasAssociatedWith\".id AS \"wasAssociatedWith_id\", \"wasAssociatedWith\".role AS \"wasAssociatedWith_role\", \"wasAssociatedWith\".activity AS \"wasAssociatedWith_activity\", \"wasAssociatedWith\".agent AS \"wasAssociatedWith_agent\" \n",
      "FROM \"wasAssociatedWith\" ORDER BY \"wasAssociatedWith\".id\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-07-30 11:06:56,040 INFO sqlalchemy.engine.base.Engine ()\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "INFO:sqlalchemy.engine.base.Engine:()\n"
     ]
    }
   ],
   "source": [
    "# Put the results in a file for the Provenance RFC\n",
    "with open(\"muons_provRFC.txt\", \"w\") as prov:\n",
    "    prov.write(\"Provenance working example - CTA ctapipe-display-muons\\n\")\n",
    "    prov.write(\"datamodel version 1.2 / preparation for PR-version 2 January 2019. MS.\\n\")\n",
    "    prov.write(\"=========================================================================\\n\")\n",
    "    prov.write(\"Remarks\\n\")\n",
    "    prov.write(\"- ActivityDescription id = activity_name + '_' + ctapipe version\\n\")\n",
    "    prov.write(\"- Activity id = uuid returned from ctapipe\\n\")  \n",
    "    prov.write(\"- Entity id = hash (file)\\n\")\n",
    "    prov.write(\"- Link between Entity and EntityDescription not defined. Via role?\\n\")\n",
    "    prov.write(\"- Used and WasGeneratedBy Ids = activity id + '_' + 'entity id or incremental?\\n\")\n",
    "    prov.write(\"\\n\")\n",
    "    prov.write(\"\\n\")\n",
    "    prov.write(\"=========================================================================\\n\")\n",
    "    prov.write(\"\\n\")\n",
    "\n",
    "    # Opérations sur le fichier\n",
    "    for classname in [ActivityDescription, EntityDescription, UsageDescription, GenerationDescription, \\\n",
    "                      DatasetDescription, ValueDescription, ParameterDescription,\\\n",
    "                      Activity, Entity, Used, WasGeneratedBy, \\\n",
    "                      DatasetEntity, ValueEntity, Parameter,\\\n",
    "                      Agent, WasAttributedTo, WasAssociatedWith]:\n",
    "        for instance in session.query(classname).order_by(classname.id):\n",
    "            prov.write(\"%s\\n\" %instance)\n",
    "prov.close()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Provenance working example - CTA ctapipe-display-muons\n",
      "datamodel version 1.2 / preparation for PR-version 2 January 2019. MS.\n",
      "=========================================================================\n",
      "Remarks\n",
      "- ActivityDescription id = activity_name + '_' + ctapipe version\n",
      "- Activity id = uuid returned from ctapipe\n",
      "- Entity id = hash (file)\n",
      "- Link between Entity and EntityDescription not defined. Via role?\n",
      "- Used and WasGeneratedBy Ids = activity id + '_' + 'entity id or incremental?\n",
      "\n",
      "\n",
      "=========================================================================\n",
      "\n",
      "ActivityDescription.id=ctapipe_display_muons_0.6.1\n",
      "ActivityDescription.name=ctapipe_display_muons\n",
      "ActivityDescription.version=0.6.1\n",
      "ActivityDescription.description=None\n",
      "ActivityDescription.type=reconstruction\n",
      "ActivityDescription.subtype=\n",
      "ActivityDescription.doculink=\n",
      "\n",
      "DatasetDescription.id=muons_hdf5\n",
      "DatasetDescription.name=muons\n",
      "DatasetDescription.type=None\n",
      "DatasetDescription.description=muon file\n",
      "DatasetDescription.doculink=None\n",
      "DatasetDescription.classType=datasetDescription\n",
      "\n",
      "DatasetDescription.id=proton_events\n",
      "DatasetDescription.name=protons\n",
      "DatasetDescription.type=None\n",
      "DatasetDescription.description=proton file\n",
      "DatasetDescription.doculink=None\n",
      "DatasetDescription.classType=datasetDescription\n",
      "\n",
      "ValueDescription.id=status\n",
      "ValueDescription.name=None\n",
      "ValueDescription.type=None\n",
      "ValueDescription.description=None\n",
      "ValueDescription.doculink=None\n",
      "ValueDescription.classType=valueDescription\n",
      "\n",
      "UsageDescription.id=ctapipe_display_muons_0.6.1_proton_events\n",
      "UsageDescription.role=dl0.sub.evt\n",
      "UsageDescription.description=None\n",
      "UsageDescription.type=None\n",
      "UsageDescription.activityDescription_id=ctapipe_display_muons_0.6.1\n",
      "UsageDescription.entityDescription_id=proton_events\n",
      "\n",
      "GenerationDescription.id=ctapipe_display_muons_0.6.1_muons_hdf5\n",
      "GenerationDescription.role=dl0.sub.evt\n",
      "GenerationDescription.description=None\n",
      "GenerationDescription.type=None\n",
      "GenerationDescription.activityDescription_id=ctapipe_display_muons_0.6.1\n",
      "GenerationDescription.entityDescription_id=muons_hdf5\n",
      "\n",
      "GenerationDescription.id=ctapipe_display_muons_0.6.1_status\n",
      "GenerationDescription.role=quality\n",
      "GenerationDescription.description=None\n",
      "GenerationDescription.type=None\n",
      "GenerationDescription.activityDescription_id=ctapipe_display_muons_0.6.1\n",
      "GenerationDescription.entityDescription_id=status\n",
      "\n",
      "DatasetDescription.id=muons_hdf5\n",
      "DatasetDescription.name=muons\n",
      "DatasetDescription.type=None\n",
      "DatasetDescription.description=muon file\n",
      "DatasetDescription.doculink=None\n",
      "DatasetDescription.classType=datasetDescription\n",
      "\n",
      "DatasetDescription.id=proton_events\n",
      "DatasetDescription.name=protons\n",
      "DatasetDescription.type=None\n",
      "DatasetDescription.description=proton file\n",
      "DatasetDescription.doculink=None\n",
      "DatasetDescription.classType=datasetDescription\n",
      "\n",
      "ValueDescription.id=status\n",
      "ValueDescription.name=None\n",
      "ValueDescription.type=None\n",
      "ValueDescription.description=None\n",
      "ValueDescription.doculink=None\n",
      "ValueDescription.classType=valueDescription\n",
      "\n",
      "Agent.id=CTAO\n",
      "Agent.name=CTA Observatory\n",
      "Agent.type=Organization\n",
      "Agent.email=None\n",
      "Agent.affiliation=None\n",
      "Agent.phone=None\n",
      "Agent.address=None\n",
      "Agent.comment=None\n",
      "Agent.url=None\n",
      "\n"
     ]
    }
   ],
   "source": [
    "# Display the file contents\n",
    "with open(\"muons_provRFC.txt\", \"r\") as prov:\n",
    "    for line in prov:\n",
    "        print (line[:-1])\n",
    "prov.close()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Visualize the provenance"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [
    {
     "ename": "ModuleNotFoundError",
     "evalue": "No module named 'prov'",
     "output_type": "error",
     "traceback": [
      "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[0;31mModuleNotFoundError\u001b[0m                       Traceback (most recent call last)",
      "\u001b[0;32m<ipython-input-10-110075069994>\u001b[0m in \u001b[0;36m<module>\u001b[0;34m\u001b[0m\n\u001b[0;32m----> 1\u001b[0;31m \u001b[0;32mimport\u001b[0m  \u001b[0mprov\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mmodel\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m      2\u001b[0m \u001b[0;32mimport\u001b[0m  \u001b[0mprov\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mdot\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      3\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      4\u001b[0m \u001b[0mprovDoc\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mprov\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mmodel\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mProvDocument\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      5\u001b[0m \u001b[0mprovDoc\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0madd_namespace\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m'voprov'\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0;34m'http://wiki.ivoa.net/twiki/bin/view/IVOA/ProvenanceDataModel/ns/'\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;31mModuleNotFoundError\u001b[0m: No module named 'prov'"
     ]
    }
   ],
   "source": [
    "import  prov.model\n",
    "import  prov.dot\n",
    "\n",
    "provDoc = prov.model.ProvDocument()\n",
    "provDoc.add_namespace('voprov', 'http://wiki.ivoa.net/twiki/bin/view/IVOA/ProvenanceDataModel/ns/')\n",
    "provDoc.add_namespace('prov', 'http://www.w3.org/ns/prov/')\n",
    "provDoc.add_namespace('cta', 'http://voparis-cta-confluence.obspm.fr/provenance/')\n",
    "provFile = \"muons_provRFC.svg\"\n",
    "\n",
    "for classname in [Activity]:\n",
    "    for instance in session.query(classname).order_by(classname.id):\n",
    "        provDoc.activity('cta:' + instance.id, startTime=instance.startTime, endTime=instance.endTime)\n",
    "for classname in [Entity, DatasetEntity]:\n",
    "    for instance in session.query(classname).order_by(classname.id):\n",
    "        provDoc.entity('cta:' + str(instance.id), {'voprov:name':instance.name})\n",
    "for classname in [ValueEntity]:\n",
    "    for instance in session.query(classname).order_by(classname.id):\n",
    "        provDoc.entity('cta:' + str(instance.id), {'voprov:name':instance.name, 'voprov:value':instance.valueXX})\n",
    "for classname in [Used]:\n",
    "    for instance in session.query(classname).order_by(classname.id):\n",
    "        provDoc.used('cta:'+instance.activity_id, 'cta:'+str(instance.entity_id))\n",
    "for classname in [WasGeneratedBy]:\n",
    "    for instance in session.query(classname).order_by(classname.id):\n",
    "        provDoc.wasGeneratedBy('cta:'+str(instance.entity_id), 'cta:'+instance.activity_id)\n",
    "for classname in [Agent]:\n",
    "    for instance in session.query(classname).order_by(classname.id):\n",
    "        provDoc.agent('cta:'+instance.id)\n",
    "for classname in [WasAssociatedWith]:\n",
    "    for instance in session.query(classname).order_by(classname.id):\n",
    "        provDoc.wasAssociatedWith('cta:'+instance.activity, 'cta:'+instance.agent)\n",
    "for classname in [WasAttributedTo]:\n",
    "    for instance in session.query(classname).order_by(classname.id):\n",
    "        provDoc.wasAttributedTo('cta:'+instance.entity, 'cta:'+instance.agent)\n",
    "\n",
    "dot = prov.dot.prov_to_dot(provDoc, use_labels=True)\n",
    "dot.write_svg(provFile)\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {},
   "outputs": [
    {
     "ename": "SyntaxError",
     "evalue": "invalid syntax (<ipython-input-11-69243ca5e5ce>, line 2)",
     "output_type": "error",
     "traceback": [
      "\u001b[0;36m  File \u001b[0;32m\"<ipython-input-11-69243ca5e5ce>\"\u001b[0;36m, line \u001b[0;32m2\u001b[0m\n\u001b[0;31m    <img src=\"muons_provRFC.svg?modified=12456780\">\u001b[0m\n\u001b[0m    ^\u001b[0m\n\u001b[0;31mSyntaxError\u001b[0m\u001b[0;31m:\u001b[0m invalid syntax\n"
     ]
    }
   ],
   "source": [
    "## Display the provenance \n",
    "<img src=\"muons_provRFC.svg?modified=12456780\">"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-07-30 11:09:02,586 INFO sqlalchemy.engine.base.Engine ROLLBACK\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "INFO:sqlalchemy.engine.base.Engine:ROLLBACK\n"
     ]
    }
   ],
   "source": [
    "session.close()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.6.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
