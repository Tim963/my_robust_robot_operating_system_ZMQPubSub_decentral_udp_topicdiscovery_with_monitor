from multiprocessing import Process
from nodes.camera_node import run_camera_node
from nodes.auto_viewer_node import run_auto_viewer_node

if __name__ == "__main__":
    camera = Process(target=run_camera_node)
    viewer = Process(target=run_auto_viewer_node)
    camera.start()
    viewer.start()
    camera.join()
    viewer.join()
