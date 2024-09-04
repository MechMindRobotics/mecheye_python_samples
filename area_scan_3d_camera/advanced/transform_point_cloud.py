# With this sample, you can obtain point cloud in a specified coordinate system.

from mecheye.shared import *
from mecheye.area_scan_3d_camera import *
from mecheye.area_scan_3d_camera_utils import find_and_connect, confirm_capture_3d
import numpy as np

class TransformPointCloud(object):
    def __init__(self):
        self.camera = Camera()
        self.frame_all_2d_3d = Frame2DAnd3D()


    def get_transformed_point_cloud(self):
        # Transform the reference frame of the point cloud and save the point cloud
        transformation = get_transformation_params(self.camera)
        frmae_3d = Frame3D(self.frame_all_2d_3d.frame_3d())
        transformed_point_cloud  =  transform_point_cloud(transformation,frmae_3d.get_untextured_point_cloud())
        point_cloud_file = "PointCloud.ply"
        show_error(Frame3D.save_point_cloud(transformed_point_cloud,FileFormat_PLY, point_cloud_file))
        print("Capture and save the point cloud: {}.".format(
            point_cloud_file))

    def get_transformed_textured_point_cloud(self):
        # Transform the reference frame of the textured point cloud and save the point cloud
        transformation = get_transformation_params(self.camera)
        transformed_textured_point_cloud  = transform_textured_point_cloud(transformation,self.frame_all_2d_3d.get_textured_point_cloud())
        textured_point_cloud_file = "TexturedPointCloud.ply"
        UntexturedPointCloud
        show_error(Frame2DAnd3D.save_point_cloud(transformed_textured_point_cloud,FileFormat_PLY,
                                                                  textured_point_cloud_file))
        print("Capture and save the textured point cloud: {}".format(
            textured_point_cloud_file))

    def get_transformed_point_cloud_with_normals(self):
       # Transform the reference frame of the point cloud with normals and save the point cloud
        transformation = get_transformation_params(self.camera)
        frmae_3d = Frame3D(self.frame_all_2d_3d.frame_3d())
        transformed_point_cloud_with_normals  =  transform_point_cloud_with_normals(transformation,frmae_3d.get_untextured_point_cloud())
        point_cloud_with_normals_file = "PointCloudWithNormals.ply"
        show_error(
            Frame3D.save_point_cloud_with_normals(transformed_point_cloud_with_normals,FileFormat_PLY, point_cloud_with_normals_file,False))
        print("Capture and save the point cloud with normals: {}.".format(
            point_cloud_with_normals_file)) 

    def get_transformed_textured_point_cloud_with_normals(self):
        # Transform the reference frame of the textured point cloud with normals and save the point cloud
        transformation = get_transformation_params(self.camera)
        transformed_textured_point_cloud_with_normals  =  transform_textured_point_cloud_with_normals(transformation,self.frame_all_2d_3d.get_textured_point_cloud())
        textured_point_cloud_with_normals_file = "TexturedPointCloudWithNormals.ply"
        show_error(Frame2DAnd3D.save_point_cloud_with_normals(transformed_textured_point_cloud_with_normals,FileFormat_PLY,
                                                                  textured_point_cloud_with_normals_file,False))
        print("Capture and save the textured point cloud: {}".format(
            textured_point_cloud_with_normals_file))            

    def main(self):
        if find_and_connect(self.camera):
            if not confirm_capture_3d():
                return
            show_error(self.camera.capture_2d_and_3d(self.frame_all_2d_3d))
            transformation = get_transformation_params(self.camera)
            # Obtain the rigid body transformation from the camera reference frame to the custom reference
            # frame
            # The custom reference frame can be adjusted using the "Custom Reference Frame" tool in
            # Mech-Eye Viewer. The rigid body transformations are automatically calculated after the
            # settings in this tool have been applied
            if(transformation.__is__valid__() == False):
                print("Transformation parameters are not set. Please configure the transformation parameters using the custom coordinate system tool in the client.")
            self.get_transformed_point_cloud()
            self.get_transformed_textured_point_cloud()
            self.get_transformed_point_cloud_with_normals()
            self.get_transformed_textured_point_cloud_with_normals()
            self.camera.disconnect()
            print("Disconnected from the camera successfully.")

if __name__ == '__main__':
    a = TransformPointCloud()
    a.main()