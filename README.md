# GeOikos
Sistema de registro y prestamo de equipo para el Grupo Excursionista Oikos

## Instalación
Si el proyecto es nuevo:
- Correr el entorno virtual con python3.
- Instalar los requirements.txt
```bash
pip install -r requirements.txt
```
- Correr el script "borrarbase". Aqui se creara la base de datos en postgres, tambien se crea un usuario en el admin de django.
```bash
./borrarbase.sh
```
Si el proyecto ya estaba iniciado:
- Correr el script "deletemigrations". Borrará todas las migraciones existentes.
```bash
./deletemigrations.sh
```
- Correr el script "borrarbase". Aqui se creara la base de datos en postgres, tambien se crea un usuario en el admin de django.
```bash
./borrarbase.sh
```

## Pruebas Unitarias
- Correr el script "testdb". Sincroniza la base de datos para los test.
```bash
./testdb.sh
```
