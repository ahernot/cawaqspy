from qgis.core import QgsProject, QgsApplication


# Initialize QGis application
PATH_QGIS = '/usr/bin/qgis'
QgsApplication.setPrefixPath(PATH_QGIS, True)
# QgsApplication.initQgis()


# Create QGis project instance
PATH_PROJECT = '$HOME/anatole/Documents/DATA_CAWAQS/SEINE_3C/Projet_SIG/Modele_Seine_Simple_DataSelected2024.qgs'
QGS_PROJECT = QgsProject.instance()
success = QGS_PROJECT.read(PATH_PROJECT)

print(success, QGS_PROJECT)
