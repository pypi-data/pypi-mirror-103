
def calibrate(self,aquiStatic, dictRef, dictAnatomic,  options=None):
    """
        Perform full CGM1 calibration.

        :Parameters:
           - `aquiStatic` (btkAcquisition) - btkAcquisition instance from a static c3d
           - `dictRef` (dict) - dictionnary reporting markers and sequence use for building **Technical** coordinate system
           - `dictAnatomic` (dict) - dictionnary reporting markers and sequence use for building **Anatomical**  coordinate system
           - `options` (dict) - use to pass options, like options altering the standard segment construction.

        .. note:: This method constructs technical and anatomical frane sucessively.

        .. warning : Foot Calibration need attention. Indeed, its technical coordinate system builder requires the anatomical coordinate system of the shank

    """
    #TODO : to input Frane init and Frame end manually

    LOGGER.logger.debug("=====================================================")
    LOGGER.logger.debug("===================CGM CALIBRATION===================")
    LOGGER.logger.debug("=====================================================")

    ff=aquiStatic.GetFirstFrame()
    lf=aquiStatic.GetLastFrame()
    frameInit=ff-ff
    frameEnd=lf-ff+1

    if self.m_bodypart !=enums.BodyPart.UpperLimb:

        if not self.decoratedModel:
            LOGGER.logger.debug(" Native CGM")
            if not btkTools.isPointExist(aquiStatic,"LKNE"):
                btkTools.smartAppendPoint(aquiStatic,"LKNE",np.zeros((aquiStatic.GetPointFrameNumber(),3) ))
            if not btkTools.isPointExist(aquiStatic,"RKNE"):
                btkTools.smartAppendPoint(aquiStatic,"RKNE",np.zeros((aquiStatic.GetPointFrameNumber(),3) ))

        else:
            LOGGER.logger.debug(" Decorated CGM")
