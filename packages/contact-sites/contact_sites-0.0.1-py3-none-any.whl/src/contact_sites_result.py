import numpy as np
from numpy.core.fromnumeric import shape
import numpy.ma as ma
import logging
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.gridspec import GridSpec
import tifffile
from itkwidgets import view

log = logging.getLogger(__name__)

"""
ContactSitesResult
------------------
Class holds output contact sites between different orgnalles

Use:

"""


class ContactSitesResult:
    def __init__(self,title) -> None:

        # legend: dictonary between overlays(number) to name and color
        bg_color = np.zeros(shape=(3),dtype=np.uint8)
        self.__metadata = {0:{
            "color":bg_color,
            "name":"Background",
            "contacts_count":0,
            "contacts_percentage":0
        }}

        # colors manager
        self.__base_colors = np.array(
            [np.array([255,0,255]),
             np.array([0,255,255]),
             np.array([255,255,0])]
        )
        self.__base_index = 0

        # overlays:
        self.__overlays = []

        # image: ndarray of all images
        self.__image = None
        self.__figure = None
        self.__title = title

        # contacts_data: array of arrays , each cell contains the numbers of the images in it's location.
        self.__contacts_data = None

        self.__add_contacts_data_vectorize = np.vectorize(self.__add_contact_data)

        self.__create_image = np.vectorize(self.__create_image_elem, signature='()->(n)')
        
        # dim distribuation number of appernces of each overlay over the the dimension
        self.__get_overlay_from_slice = np.vectorize(self.is_contain_overlay)
        
        self.__is_figure_dirty = False
        self.__is_image_dirty = False
        self.__is_metadata_dirty = False

    def set_title(self,title) -> None:
        self.__title = title
        return None

    def get_metadata(self) -> dict:
        if (self.__is_metadata_dirty):
            sum_contacts = np.count_nonzero(self.__contacts_data)
            unique_elems, counts = np.unique(self.__contacts_data, return_counts=True)
            num_of_unique_elements = len(unique_elems[1:])
            for i in range(1,num_of_unique_elements + 1):
                contacts = unique_elems[i]
                contacts_count = counts[i]
                name = None
                color = None
                for overlay in self.__overlays:
                    if (self.is_contain_overlay(contacts,overlay.get("index"))):
                        if (name is None):
                            name = overlay.get("name")
                            color = overlay.get("base_color")
                        else:
                            name = "{}-{}".format(name,overlay.get("name"))
                            color = self.__add_colors(color, overlay.get("base_color"))
                self.__metadata[contacts] = {
                    "color":color,
                    "name":name,
                    "contacts_count":contacts_count,
                    "contacts_percentage":contacts_count/sum_contacts
                }
            self.__is_metadata_dirty = False
        return self.__metadata

    def get_image(self) -> np.ndarray:
        if (self.__is_image_dirty):
            if ((self.__image is None) and ~(self.__contacts_data is None)):
                self.__image = np.zeros(shape=(*self.__contacts_data.shape,3), dtype=np.uint8)
            self.__image = self.__create_image(self.__contacts_data)
            self.__is_image_dirty = False
        return self.__image

    def __get_slice_image(self,slice):
        return self.get_image()[slice]

    def __create_image_elem(self,overlays) -> np.ndarray:
        return self.__metadata[overlays]["color"]

    # def __create_random_color(self) -> np.ndarray:
    #     return np.random.rand(3) * 255

    # color utils
    def __get_base_color(self):
        color = self.__base_colors[self.__base_index % 3]
        self.__base_index = self.__base_index + 1
        if (self.__base_index >= len(self.__base_colors)):
            self.__base_colors = self.__base_colors / 2
        return color

    def __add_colors(self,c1,c2):
        return (c1 + c2) / 2

    def __add_contact_data(self,overly_elem,contacts_data_elem,overlay_index) -> np.uint32:
        if (overly_elem > 0):
            contacts_data_elem = (contacts_data_elem) | pow(2,overlay_index)
        return contacts_data_elem

    def add_overlay(self,overlay:np.ndarray,legend_name:str) -> None:
        self.__is_image_dirty = True
        self.__is_metadata_dirty = True
        self.__is_figure_dirty = True
        index = len(self.__overlays)
        self.__overlays.append({
            "name":legend_name,
            "index":index,
            "base_color":self.__get_base_color()
        })

        if (self.__contacts_data is None):
            self.__contacts_data = np.zeros(shape=overlay.shape, dtype=np.uint32)

        self.__contacts_data = self.__add_contacts_data_vectorize(overlay,self.__contacts_data,index)

    def get_overlayes_metadata(self) -> list:
        return self.__overlays

    def get_contacts_data(self) -> np.ndarray:
        return self.__contacts_data

    def is_contain_overlay(self,overlays,overlay_index) -> bool:
        return (overlays & pow(2,overlay_index) > 0)
    
    def get_dim_distribuation(self,dim)->np.array:
        max_dims = self.__contacts_data.shape
        num_of_dims = len(max_dims)
        num_overlays = len(self.__overlays)
        curr_dims_start = np.zeros(shape=(num_of_dims))
        curr_dims_end = max_dims
        distribuation = np.array(shape=(max_dims[dim],num_overlays))
        for i in range(max_dims[dim]):
            curr_dims_start[dim]=i
            curr_dims_end[dim]=i+1
            if (num_of_dims==2):
                contacts_data_slice = self.__contacts_data[curr_dims_start[0]:curr_dims_end[0],curr_dims_start[1]:curr_dims_end[1]]    
            elif (num_of_dims==3):
                contacts_data_slice = self.__contacts_data[curr_dims_start[0]:curr_dims_end[0],curr_dims_start[1]:curr_dims_end[1],curr_dims_start[2]:curr_dims_end[2]]   
            elif (num_of_dims==4):
                contacts_data_slice = self.__contacts_data[curr_dims_start[0]:curr_dims_end[0],curr_dims_start[1]:curr_dims_end[1],curr_dims_start[2]:curr_dims_end[2],curr_dims_start[3]:curr_dims_end[3]]   
            else:
                print("get_dim_distribuation supports only 2,3 or 4 dimensions , curr dimensions number is {}".format(num_of_dims))
                return None
            
            for overlay in self.__overlays.values():
                overlay_index = overlay["index"]
                overlay_apperances = self.__get_overlay_from_slice(contacts_data_slice,overlay_index)
                distribuation[i,overlay_index] = np.sum(overlay_apperances)
        return distribuation
        
    def save_distribuation_figure(dim)->None:
        distribuation = self.get_dim_distribuation(dim)
        num_slices = distribuation.shape[0]
        metadata = self.get_metadata()
        
        return None
        

    def get_figure(self,figure_ratio=4,image_to_legend_ratio=1):
        if (self.__is_figure_dirty):
            labels = []
            handles = []
            image = self.get_image()
            num_slices = image.shape[0]
            # create legend in plot
            metadata = self.get_metadata()
            for overlays in metadata.values():
                labels.append("{}:{}:{:.2f}%".format(overlays["name"],overlays["contacts_count"],overlays["contacts_percentage"]*100))
                handles.append(Rectangle((0,0),1,1, color=overlays["color"] / 255))

            rows = int(np.sqrt(num_slices) * image_to_legend_ratio) + 1
            cols = int(np.sqrt(num_slices))
            self.__figure = plt.figure(figsize=(rows * figure_ratio,cols * figure_ratio))
            gs = self.__figure.add_gridspec(rows,cols)
            ax = self.__figure.add_subplot(gs[:-1,:])
            ax2 = self.__figure.add_subplot(gs[-1,:])
            slice = 0
            for i in range(0,rows - 1,image_to_legend_ratio):
                for j in range(cols):
                    temp_ax = self.__figure.add_subplot(gs[i:i + image_to_legend_ratio,j])
                    temp_ax.imshow(self.__get_slice_image(slice))
                    temp_ax.axis('off')
                    slice += 1

            ax.set_title(self.__title,fontsize=50)
            ax2.legend(handles,labels, mode='expand', ncol=3,fontsize=30)
            ax2.axis('off')
            ax.axis('off')
            self.__is_figure_dirty = False

        return self.__figure

    def plot_figure(self,figure_ratio=4,image_to_legend_ratio=1):
        self.get_figure(figure_ratio=4,image_to_legend_ratio=1)
        plt.show()

    def save_figure(self,path,figure_ratio=4,image_to_legend_ratio=1):
        self.get_figure(figure_ratio=4,image_to_legend_ratio=1)
        plt.savefig(path)

    def save_tiff(self,path):
        tifffile.imsave(path,self.get_image(),self.get_image().shape)
        
    def save_greyscale_tiff(self,path):
        image_gs = self.__get_image_greyscale()
        tifffile.imsave(path,image_gs,image_gs.shape)
        
    def view_tiff(self):
        view(self.__get_image_greyscale())
        
    def __get_image_greyscale(self):
        im = self.get_image()
        if (len(im.shape) == 4):
            im = np.average(im,axis=3)
        assert len(im.shape) == 3

        im = im.astype(np.float32)
        im = (im - im.min()) / (im.max() - im.min())

        return im
