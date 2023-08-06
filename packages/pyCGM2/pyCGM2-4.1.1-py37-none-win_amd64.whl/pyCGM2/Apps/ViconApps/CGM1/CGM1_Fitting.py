# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""Nexus Operation : **CGM1 Fitting**

:param --proj [string]: define in which coordinate system joint moment will be expressed (Choice : Distal, Proximal, Global)
:param -md, --markerDiameter [int]: marker diameter
:param -ps, --pointSuffix [string]: suffix adds to the vicon nomenclature outputs
:param --check [bool]: add "cgm1" as point suffix


Examples:
    In the script argument box of a python nexus operation, you can edit:

    >>> --proj=Global
    (means joint moments will be expressed into the Global Coordinate system)

"""

#import ipdb
import os
import pyCGM2; LOGGER = pyCGM2.LOGGER
import argparse
import warnings
warnings.filterwarnings("ignore")

# pyCGM2 settings
import pyCGM2


# vicon nexus
from viconnexusapi import ViconNexus

# pyCGM2 libraries
from pyCGM2.Configurator import CgmArgsManager
from pyCGM2.Lib.CGM import  cgm1


from pyCGM2.Utils import files
from pyCGM2.Nexus import nexusFilters,nexusTools,nexusUtils


def main():

    NEXUS = ViconNexus.ViconNexus()
    NEXUS_PYTHON_CONNECTED = NEXUS.Client.IsConnected()

    parser = argparse.ArgumentParser(description='CGM1 Fitting')
    parser.add_argument('--proj', type=str, help='Moment Projection. Choice : Distal, Proximal, Global')
    parser.add_argument('-md','--markerDiameter', type=float, help='marker diameter')
    parser.add_argument('-ps','--pointSuffix', type=str, help='suffix of model outputs')
    parser.add_argument('--check', action='store_true', help='force model output suffix')
    parser.add_argument('-ae','--anomalyException', action='store_true', help='stop if anomaly detected ')
    parser.add_argument('-fi','--frameInit',type=int,  help='first frame to process')
    parser.add_argument('-fe','--frameEnd',type=int,  help='last frame to process')

    args = parser.parse_args()

    if NEXUS_PYTHON_CONNECTED: # run Operation
        # --------------------------GLOBAL SETTINGS ------------------------------------
        # global setting ( in user/AppData)
        if os.path.isfile(pyCGM2.PYCGM2_APPDATA_PATH + "CGM1-pyCGM2.settings"):
            settings = files.openFile(pyCGM2.PYCGM2_APPDATA_PATH,"CGM1-pyCGM2.settings")
        else:
            settings = files.openFile(pyCGM2.PYCGM2_SETTINGS_FOLDER,"CGM1-pyCGM2.settings")

        # --------------------------CONFIG ------------------------------------
        argsManager = CgmArgsManager.argsManager_cgm1(settings,args)
        markerDiameter = argsManager.getMarkerDiameter()
        pointSuffix = argsManager.getPointSuffix("cgm1")
        momentProjection =  argsManager.getMomentProjection()

        DATA_PATH, reconstructFilenameLabelledNoExt = NEXUS.GetTrialName()

        reconstructFilenameLabelled = reconstructFilenameLabelledNoExt+".c3d"
        LOGGER.logger.info( "data Path: "+ DATA_PATH )
        LOGGER.set_file_handler(DATA_PATH+"pyCGM2-Fitting.log")
        LOGGER.logger.info( "calibration file: "+ reconstructFilenameLabelled)

        # --------------------------SUBJECT ------------------------------------
        # Notice : Work with ONE subject by session
        subjects = NEXUS.GetSubjectNames()
        subject = nexusTools.getActiveSubject(NEXUS)
        LOGGER.logger.info(  "Subject name : " + subject  )

        # --------------------pyCGM2 MODEL ------------------------------
        model = files.loadModel(DATA_PATH,subject)

        # -------------------------- MP ------------------------------------
        # allow alteration of thigh offset
        model.mp_computed["LeftThighRotationOffset"] =   NEXUS.GetSubjectParamDetails( subject, "LeftThighRotation")[0]
        model.mp_computed["RightThighRotationOffset"] =   NEXUS.GetSubjectParamDetails( subject, "RightThighRotation")[0]

        # --------------------------CHECKING -----------------------------------
        # check model is the CGM1
        LOGGER.logger.info("loaded model : %s" %(model.version ))
        if model.version != "CGM1.0":
            raise Exception ("%s-pyCGM2.model file was not calibrated from the CGM1.0 calibration pipeline"%model.version)

        # --------------------------SESSION INFOS ------------------------------------

        #  translators management
        translators = files.getTranslators(DATA_PATH,"CGM1.translators")
        if not translators:  translators = settings["Translators"]

        #force plate assignement from Nexus
        mfpa = nexusTools.getForcePlateAssignment(NEXUS)

        # btkAcq builder
        nacf = nexusFilters.NexusConstructAcquisitionFilter(DATA_PATH,reconstructFilenameLabelledNoExt,subject)
        acq = nacf.build()
        # --------------------------MODELLING PROCESSING -----------------------
        acqGait,detectAnomaly = cgm1.fitting(model,DATA_PATH, reconstructFilenameLabelled,
            translators,
            markerDiameter,
            pointSuffix,
            mfpa,momentProjection,
            forceBtkAcq=acq,
            anomalyException=args.anomalyException,
            frameInit= args.frameInit, frameEnd= args.frameEnd )

        # ----------------------SAVE-------------------------------------------
        # Todo: pyCGM2 model :  cpickle doesn t work. Incompatibility with Swig. ( see about BTK wrench)


        # ----------------------DISPLAY ON VICON-------------------------------
        nexusFilters.NexusModelFilter(NEXUS,model,acqGait,subject,pointSuffix).run()
        nexusTools.createGeneralEvents(NEXUS,subject,acqGait,["Left-FP","Right-FP"])





    else:
        raise Exception("NO Nexus connection. Turn on Nexus")


if __name__ == "__main__":

    main()
