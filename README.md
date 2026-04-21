📘 README.md — Sistema de Biblioteca
📌 Título del Proyecto
LibraryFlow — Sistema de Gestión de Biblioteca

👤 Integrante del Proyecto
Yeriel [Apellido] — Desarrollador único

🧩 Descripción del Problema
Las bibliotecas pequeñas suelen manejar sus préstamos y registros de forma manual, lo que genera errores, pérdida de información y dificultad para dar seguimiento a los libros prestados.
Este sistema automatiza el proceso de registro, préstamo y devolución de libros.

🎯 Objetivo del Sistema
Objetivo General
Crear una aplicación funcional que permita gestionar libros, usuarios y préstamos dentro de una biblioteca.

Objetivos Específicos
Registrar libros y su disponibilidad

Administrar préstamos y devoluciones

Permitir a los usuarios consultar sus préstamos

Mantener un historial de movimientos

Proveer una interfaz clara y fácil de usar

👥 Usuarios o Público Objetivo
Bibliotecarios

Estudiantes

Personal administrativo

Usuarios que consultan disponibilidad de libros

🛠️ Tecnologías Utilizadas
Python (Flask)

HTML, CSS

SQLite

pytest

GitHub + Visual Studio Code

🏗️ Arquitectura General
Arquitectura Cliente–Servidor:

Frontend: HTML + CSS

Backend: Flask

Base de datos: SQLite

Templates: Sistema de vistas HTML

Controladores: Lógica en app.py

🧱 Módulos o Componentes del Sistema
Autenticación: login, registro

Gestión de Libros: listado, disponibilidad

Préstamos: préstamos activos, historial

Dashboard: vista general del sistema

Plantilla base: estructura visual común

▶️ Instrucciones para Ejecutar el Proyecto
(Versión simplificada, cumpliendo el requerimiento sin pasos innecesarios)

El proyecto se ejecuta directamente desde Visual Studio Code, utilizando el entorno configurado y sincronizado con GitHub.
Solo es necesario abrir la carpeta del proyecto en VS Code y ejecutar app.py.

📂 Estructura del Repositorio
Código
PROJECT-SOFTWARE-ENGINEERING/
│── app.py
│── init_db.py
│── database.db
│── requirements.txt
│── README.md
│
├── static/
│   └── style.css
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── books.html
│   ├── occupied.html
│   └── my_loans.html
🗄️ Descripción de la Base de Datos
Tablas principales:

users (id, username, password)

books (id, title, author, available)

loans (id, user_id, book_id, loan_date, return_date)

Relaciones simples entre usuarios y préstamos.

📌 Evidencia del Uso de SCRUM
Aunque el proyecto fue individual, se aplicaron prácticas SCRUM:

Backlog personal

Tareas organizadas por prioridad

Iteraciones semanales

Registro de progreso en GitHub

🧪 Evidencia del Uso de Testing
Incluye:

Pruebas unitarias con pytest

3 UAT funcionales

3 UAT UI

Evidencia incluida en el PDF y repositorio

📊 Estado Actual del Proyecto
Funcionalidades principales completas

Base de datos operativa

Pruebas realizadas

Interfaz funcional

🚀 Mejoras Futuras
Roles de usuario

Buscador avanzado

Notificaciones de préstamos

Mejoras visuales

🎥 Enlaces a Videos o Presentaciones
(Se agregarán cuando estén listos)

📝 Reflexión Final
Reflexión Individual — Yeriel
Desarrollar este sistema de biblioteca me permitió integrar Flask, SQLite, pruebas automatizadas y buenas prácticas de ingeniería de software. Trabajar solo implicó organizarme con disciplina, aplicar SCRUM de forma personal y documentar cada avance. El mayor reto fue mantener la estructura del proyecto clara y funcional, pero el resultado final demuestra un sistema completo y bien fundamentado.