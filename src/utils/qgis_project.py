import os
from qgis.core import QgsProject, QgsApplication
from src.config import PATH_QGIS

os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = '/usr/lib/aarch64-linux-gnu/qt5/plugins/platforms'


# Initialize QGis application
QgsApplication.setPrefixPath(PATH_QGIS, True)
qgs_application = QgsApplication([], GUIenabled=False)
qgs_application.initQgis()


# Create QGis project instance
PATH_PROJECT = '/home/anatole/Documents/DATA_CAWAQS/SEINE_3C/Projet_SIG/Modele_Seine_Simple_DataSelected2024.qgs'
QGS_PROJECT = QgsProject.instance()
success = QGS_PROJECT.read(PATH_PROJECT)


# TODO: at the end of the code
def exit():
    qgs_application.exitQgis()
