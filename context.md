---

### ✅ **Capstone: Sistema de Reportes Financieros Personales o Empresariales**

**Objetivo:** una app donde el usuario carga ingresos, gastos, inversiones y obtiene reportes visuales y estadísticas financieras.

---

## 📈 **Features**

1. **Registro y login con JWT / OAuth2.**
2. **Roles: usuario normal vs admin.**
3. **Carga de movimientos:**
    - Tipo: ingreso / gasto / inversión.
    - Monto.
    - Fecha.
    - Categoría.
4. **Consulta de movimientos con filtros:**
    - Por fecha, tipo, categoría.
5. **Dashboard de reportes:**
    - Balance mensual.
    - Distribución de gastos por categoría.
    - Evolución del ahorro o inversión.
6. **Exportar datos en CSV o PDF.**
7. **Envío de reportes por email (tarea en background con Celery + Redis).**
8. **API versionada (`/v1/...`).**
9. **Integración con APIs externas:**
    - Cotizaciones de dólar, cripto.
    - Inflación (INDEC, por ejemplo).
10. **Logging estructurado.**
11. **Tests unitarios, integración, base de datos.**
12. **Deploy productivo con Docker + CI/CD.**

---

## 🧠 **Skills que vas a aprender**

| Feature | Skill |
| --- | --- |
| Auth con JWT | Seguridad, OAuth2 |
| Roles y permisos | Autorización avanzada |
| CRUD de movimientos | SQLAlchemy, Pydantic, arquitectura limpia |
| Filtros en queries | SQL avanzado, queries dinámicas |
| Reportes y métricas | Agregaciones, lógica de negocio |
| CSV/PDF export | Generación de archivos, librerías como `reportlab` o `weasyprint` |
| Background tasks | Celery + Redis |
| Emails | Integración SMTP o servicios externos (Sendgrid, Mailgun) |
| APIs externas | Consumo con `httpx` |
| Logging | Configuración profesional con contexto |
| Tests | pytest, testcontainers para DB |
| Deploy | Docker, docker-compose, GitHub Actions, Nginx |
| Observabilidad | Health checks, métricas, Prometheus |

---

## 🗂️ **Arquitectura**

```
/app
    /routers
    /schemas
    /models
    /crud
    /services (PDF, email, reportes)
    /core (auth, config, logging)
    /db
/tests
/docker-compose.yml
/Dockerfile
/README.md

```

---

## ✅ **Bonus**

Podés hacer una interfaz frontend o un cliente CLI, pero el foco es el **backend robusto**.

---

### Si querés te paso:

- Roadmap por sprints.
- Plantilla de repo inicial.
- Prioridad de features para no ahogarte.

¿Querés que te arme eso?