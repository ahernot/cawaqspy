from qgis.core import QgsProject, QgsApplication
# from src.config import PATH_QGIS
PATH_QGIS = '/usr/bin/qgis'


# Initialize QGis application
QgsApplication.setPrefixPath(PATH_QGIS, True)
qgs_application = QgsApplication([], GUIenabled=False)
qgs_application.initQgis()


# Create QGis project instance
# PATH_PROJECT = '$HOME/anatole/Documents/DATA_CAWAQS/SEINE_3C/Projet_SIG/Modele_Seine_Simple_DataSelected2024.qgs'
QGS_PROJECT = QgsProject.instance()
# success = QGS_PROJECT.read(PATH_PROJECT)

# print(success, QGS_PROJECT)


# qgs_application.exitQgis()  # TODO: at the end of the code