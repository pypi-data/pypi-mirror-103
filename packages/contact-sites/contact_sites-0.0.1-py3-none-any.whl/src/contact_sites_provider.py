import numpy as np
import numpy.ma as ma
import logging
import typing
from typing import Optional

from aicsimageio import AICSImage

from src.contact_sites.contact_sites_result import ContactSitesResult

log = logging.getLogger(__name__)

"""
ContactSitesFinder
------------------
Class that helps find and output contact sites between different orgnalles

image_to_ndarray: function that recive image in data and return the image as ndarray

segmentor: get image as ndarray and returns it's segmentation ndarray

"""


class ContactSitesProvider:
    def __init__(self, image_to_ndarray=None, segmentor=None, unifier=None) -> None:
        if (segmentor is not None):
            self.segmentor = segmentor
        else:
            self.segmentor = self.__default_segmentor

        if (image_to_ndarray is not None):
            self.image_to_ndarray = image_to_ndarray
        else:
            self.image_to_ndarray = self.__default_image_to_ndarray
            
        if (unifier is not None):
            self.unifier = unifier
        else:
            self.unifier = self.__default_slice_unifier

    def run_pipe(self,images,title="Title",image_to_ndarray=None,segmentor=None,unifier=None,result=None) -> ContactSitesResult:
        if (result is None):
            result = ContactSitesResult(title)
        elif (title is not None):
            result.set_title(title)
            
        for image in images:
            overlay = None
            if (image_to_ndarray is None):
                image_ndarray = self.image_to_ndarray(image.get("data"))
            else:
                image_ndarray = image_to_ndarray(image.get("data"))
                
            if (segmentor is None):
                segmentation = self.segmentor(image_ndarray)
            else:
                segmentation = segmentor(image_ndarray)
                
            if (unifier is None):
                unified = self.unifier(segmentation)
            elif (unifier is not None and unifier!=False):
                unified = segmentor(image_ndarray)
            else:
                unified = segmentation
            result.add_overlay(unified,image.get("legend_name"))
        return result

    def __default_segmentor(self,image):
        return image

    def __default_image_to_ndarray(self,image,pattern="CYX"):
        return image.get_image_data(pattern)
    
    def __default_slice_unifier(self,image):
        return np.max(image,axis=0,keepdims=True)
        
        
        
