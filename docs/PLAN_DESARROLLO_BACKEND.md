# 📋 PLAN DE DESARROLLO - API GESTIÓN DE TALLERES MECÁNICOS

> **Fecha de creación:** $(date)
> **Versión:** 1.0
> **Proyecto:** FastAPI async + SQLAlchemy async + PostgreSQL

---

## 1. DIAGNÓSTICO ACTUAL

### ✅ PARTES CUBIERTAS (Lo que ya existe)

| Capa | Módulo | Estado |
|------|--------|--------|
| **Modelos** | Workshop, User, Customer, Vehicle, WorkOrder, WorkOrderItem | ✅ Completo |
| **Enums** | TipoVehiculo, StatusWorkOrder, WorkOrderItemType | ✅ Completo |
| **Schemas** | customer, vehicle, work_order, work_order_item, user, workshop | ✅ Completo |
| **Servicios** | customer_service, vehicle_service, workorder_service | ✅ Básicos |
| **Rutas API** | auth, customers, vehicles, workOrder, workorder_item | ✅ CRUD básico |
| **Seguridad** | JWT, password hashing, OAuth2 | ✅ Implementado |

### ❌ PARTES FALTANTES (Gaps identificados)

| Módulo | Problema | Impacto |
|--------|----------|---------|
| **Roles/Permisos** | No existen tablas `roles`, `user_roles` ni lógica de autorización por rol | CRÍTICO |
| **Status Logs** | No existe modelo ni endpoints para historial de estados | ALTO |
| **Workshops** | Solo stub vacío en router, sin servicios | ALTO |
| **Usuarios** | Sin CRUD para gestionar usuarios por taller | ALTO |
| **Validaciones** | Faltan validaciones de unicidad (email, username, plate, document_id) | ALTO |
| **Paginación** | No implementada en ningún listado | MEDIO |
| **Filtros** | Endpoints de búsqueda muy limitados | MEDIO |
| **Cálculos** | No hay totales por orden (labor + parts) | BAJO |

---

## 2. LISTA PRIORIZADA DE TAREAS

### 🔴 PRIORIDAD CRÍTICA (Bloqueantes para funcionamiento básico)

#### 2.1 Sistema de Roles y Permisos
**Objetivo:** Implementar autenticación completa multi-taller con roles

| # | Tarea | Descripción |
|---|-------|-------------|
| 1.1 | **Crear modelos de roles** | Crear `models/role.py` con tablas `roles` y `user_roles` |
| 1.2 | **Crear schemas de roles** | `schemas/role.py` con RoleCreate, RoleRead, UserRoleAssign |
| 1.3 | **Crear servicio de roles** | `services/role_service.py` con CRUD de roles y asignación a usuarios |
| 1.4 | **Actualizar modelo User** | Agregar relación many-to-many a roles |
| 1.5 | **Actualizar seguridad** | Agregar dependencia `require_role(allowed_roles: list)` |
| 1.6 | **Crear routers de roles** | `api/v1/roles.py` y actualizar `users.py` para asignar roles |

#### 2.2 Gestión de Talleres (Workshops)
**Objetivo:** CRUD completo de talleres

| # | Tarea | Descripción |
|---|-------|-------------|
| 2.1 | **Crear workshop_service** | Lógica de negocio para talleres |
| 2.2 | **Completar router workshops** | GET, POST, PUT, DELETE de talleres |
| 2.3 | **Agregar filtros** | Por nombre, owner |

#### 2.3 Gestión de Usuarios
**Objetivo:** CRUD de usuarios por taller

| # | Tarea | Descripción |
|---|-------|-------------|
| 3.1 | **Crear user_service** | Lógica de negocio para usuarios |
| 3.2 | **Crear router users** | CRUD completo filtrado por shop_id |
| 3.3 | **Validar unicidad** | Verificar `UNIQUE (shop_id, email)` y `UNIQUE (shop_id, username)` |

---

### 🟠 PRIORIDAD ALTA (Funcionalidad esencial)

#### 2.4 Historial de Estados (Status Logs)
**Objetivo:** Trazabilidad de cambios de estado en órdenes

| # | Tarea | Descripción |
|---|-------|-------------|
| 4.1 | **Crear modelo status_logs** | Tabla con work_order_id, old_status, new_status, reason, changed_at |
| 4.2 | **Crear schema status_log** | StatusLogCreate, StatusLogRead |
| 4.3 | **Crear servicio status_logs** | Lógica para registrar y consultar historial |
| 4.4 | **Integrar en WorkOrder update** | Cada cambio de status debe crear un log automáticamente |
| 4.5 | **Crear endpoint historial** | `GET /workorders/{id}/status-logs` |

#### 2.5 Validaciones de Negocio
**Objetivo:** Asegurar integridad de datos

| # | Tarea | Descripción |
|---|-------|-------------|
| 5.1 | **Validar unicidad customers** | `UNIQUE (shop_id, document_id)` en create/update |
| 5.2 | **Validar unicidad vehicles** | `UNIQUE (shop_id, plate)` en create/update |
| 5.3 | **Validar vehículo-taller coherencia** | El customer del vehicle debe pertencer al mismo shop |
| 5.4 | **Validar work_order-vehicle** | La orden debe usar vehicle del mismo shop |

---

### 🟡 PRIORIDAD MEDIA (Mejora de experiencia)

#### 2.6 Paginación y Filtros
**Objetivo:** Listados escalables

| # | Tarea | Descripción |
|---|-------|-------------|
| 6.1 | **Crear esquema de paginación** | GenericResponse con items, total, page, limit |
| 6.2 | **Implementar paginación en customers** | ?page=1&limit=20 |
| 6.3 | **Implementar paginación en vehicles** | ?page=1&limit=20 |
| 6.4 | **Implementar paginación en work_orders** | ?page=1&limit=20 |
| 6.5 | **Agregar filtros en work_orders** | Por status, vehicle_id, customer_id, fecha |

#### 2.7 Cálculos y Estadísticas
**Objetivo:** Información de negocio

| # | Tarea | Descripción |
|---|-------|-------------|
| 7.1 | **Calcular totales por orden** | Sumar labor + parts del work_order |
| 7.2 | **Endpoint resumen de orden** | Devolver orden con totales calculados |
| 7.3 | **Buscar clientes por nombre** | LIKE %name% |
| 7.4 | **Buscar vehículos por marca/modelo** | LIKE %brand% |

---

### 🟢 PRIORIDAD BAJA (Extras)

| # | Tarea | Descripción |
|---|-------|-------------|
| 8.1 | **Soft delete** | Añadir campo `is_deleted` a entidades |
| 8.2 | **Dashboard stats** | Contar órdenes por estado, clientes nuevos, etc. |
| 8.3 | **Exportación** | Endpoints para exportar a CSV/PDF |

---

## 3. MINI-CHECKLIST POR MÓDULO

### 📦 MÓDULO: ROLES Y PERMISOS

**Archivos a crear:**
- `app/models/role.py` → Role, UserRole (tabla many-to-many)
- `app/schemas/role.py` → RoleCreate, RoleRead, UserRoleUpdate
- `app/services/role_service.py` → create_role, get_roles, assign_role_to_user
- `app/api/v1/roles.py` → CRUD roles, GET /users/{id}/roles, POST /users/{id}/roles
- `app/core/security.py` → agregar `require_role(roles: List[str])` dependency

**Endpoints sugeridos:**
```
GET    /roles                      # Listar todos los roles
POST   /roles                      # Crear rol
GET    /roles/{id}                 # Obtener rol por ID
PUT    /roles/{id}                 # Actualizar rol
DELETE /roles/{id}                 # Eliminar rol
GET    /users/{id}/roles           # Ver roles de usuario
POST   /users/{id}/roles           # Asignar rol a usuario
DELETE /users/{id}/roles/{role_id} # Quitar rol a usuario
```

**Validaciones obligatorias:**
- Solo usuarios con rol `ADMIN` pueden crear/eliminar roles
- Verificar que el rol existe antes de asignar
- No permitir asignar el mismo rol dos veces al mismo usuario

**Tests recomendados:**
- Crear rol nuevo (201)
- Asignar rol a usuario (201)
- Asignar rol duplicado (409 Conflict)
- Usuario sin permiso recibe 403

---

### 📦 MÓDULO: TALLERES (WORKSHOPS)

**Archivos a crear/actualizar:**
- `app/services/workshop_service.py` → crear
- `app/api/v1/workshops.py` → actualizar (solo stub)

**Endpoints sugeridos:**
```
GET    /workshops                      # Listar talleres (solo ADMIN global)
POST   /workshops                      # Crear taller
GET    /workshops/{id}                 # Obtener taller
PUT    /workshops/{id}                 # Actualizar taller
DELETE /workshops/{id}                 # Eliminar taller (solo ADMIN)
```

**Validaciones obligatorias:**
- `name` obligatorio
- Verificar unicidad de nombre si aplica

**Tests recomendados:**
- Crear taller sin nombre (422)
- Crear taller exitoso (201)
- Obtener taller existente (200)

---

### 📦 MÓDULO: USUARIOS

**Archivos a crear/actualizar:**
- `app/services/user_service.py` → crear
- `app/api/v1/users.py` → crear
- `app/models/user.py` → agregar relación a roles
- `app/schemas/user.py` → agregar UserCreate, UserUpdate (ya existe parcial)

**Endpoints sugeridos:**
```
GET    /workshops/{shop_id}/users              # Listar usuarios del taller
POST   /workshops/{shop_id}/users              # Crear usuario en taller
GET    /workshops/{shop_id}/users/{id}         # Obtener usuario
PUT    /workshops/{shop_id}/users/{id}         # Actualizar usuario
DELETE /workshops/{shop_id}/users/{id}         # Eliminar usuario (soft/hard)
PUT    /workshops/{shop_id}/users/{id}/active  # Activar/desactivar usuario
```

**Validaciones obligatorias:**
- `shop_id` obligatorio y debe existir
- `username`, `full_name`, `email`, `password` obligatorios
- `UNIQUE (shop_id, email)` → verificar antes de crear
- `UNIQUE (shop_id, username)` → verificar antes de crear
- Nunca devolver `password` en respuestas

**Errores esperados:**
- 409 Conflict si email/username ya existe en ese shop
- 404 si shop no existe

**Tests recomendados:**
- Crear usuario con email duplicado (409)
- Crear usuario exitoso (201)
- Login con usuario nuevo (200)
- Actualizar usuario (200)

---

### 📦 MÓDULO: STATUS LOGS

**Archivos a crear:**
- `app/models/status_log.py` → crear
- `app/schemas/status_log.py` → StatusLogCreate, StatusLogRead
- `app/services/status_log_service.py` → crear
- `app/api/v1/status_logs.py` → crear (o integrar en workOrder.py)

**Endpoints sugeridos:**
```
GET    /workorders/{work_order_id}/status-logs  # Historial de estados
POST   /workorders/{work_order_id}/status-logs # Registrar cambio manual (opcional)
```

**Lógica de negocio (integrar en workorder_service):**
- Al cambiar `work_orders.status`, automáticamente crear registro en `status_logs`
- Guardar `old_status` (anterior), `new_status` (nuevo), `reason`

**Validaciones obligatorias:**
- `work_order_id` debe existir y pertenecer al shop del usuario
- `new_status` debe ser uno de los valores permitidos
- `reason` obligatorio

**Tests recomendados:**
- Cambio de estado crea log automáticamente
- Listar historial de una orden (200)
- Historial vacío para orden nueva

---

### 📦 MÓDULO: WORK ORDER - MEJORAS

**Mejoras sobre lo existente:**
- Agregar paginación
- Agregar filtros
- Integrar status_logs en updates
- Agregar endpoint de cambio de estado dedicado

**Endpoints adicionales sugeridos:**
```
PATCH  /workorders/{id}/status              # Cambio de estado dedicado
GET    /workorders/{id}/summary             # Resumen con totales calculados
GET    /workorders?status=IN_PROGRESS&page=1&limit=20  # Filtrado
```

**Validaciones adicionales:**
- No permitir cambiar status a COMPLETED si hay items sin completar (opcional)
- Validar transiciones de estado permitidas (opcional)

---

## 4. CONSIDERACIONES TRANSVERSALES

### 🔐 Autenticación y Autorización

| Aspecto | Recomendación |
|---------|---------------|
| **Dependencia actual** | `current_user` ya retorna el usuario autenticado |
| **Nuevo requisito** | Agregar `require_role(*allowed_roles)` que verifique roles del usuario |
| **Shop isolation** | TODOS los endpoints deben usar `current_user.shop_id` para filtrar |
| **Super admin** | Considerar flag `is_superadmin` en User para acceder a todos los talleres |

### 🏢 Multi-Tenant (shop_id)

```python
# Patrón a seguir en TODOS los endpoints:
@router.get("/users")
async def list_users(
    current_user: Annotated[User, Depends(current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    # ✅ SIEMPRE filtrar por shop_id del usuario actual
    result = await db.execute(
        select(User).where(User.shop_id == current_user.shop_id)
    )
```

### 📄 Paginación (Patrón sugerido)

```python
# Schema genérico
from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    limit: int
    total_pages: int

# Uso: GET /customers?page=1&limit=20
```

### ⚠️ Manejo de Errores

| Código | Uso |
|--------|-----|
| 400 | Bad Request - datos inválidos |
| 401 | No autenticado |
| 403 | Autenticado pero sin permiso (rol) |
| 404 | Recurso no encontrado |
| 409 | Conflicto (duplicado) |
| 422 | Validación de Pydantic fallida |
| 500 | Error interno del servidor |

---

## 5. RESUMEN DE PRIORIDAD DE IMPLEMENTACIÓN

```
FASE 1 (Crítica) - Semanas 1-2
├── 1.1 Modelos de Roles + UserRoles
├── 1.2 Schemas de Roles
├── 1.3 Servicios de Roles
├── 1.4 Router de Roles + require_role()
├── 1.5 CRUD Talleres (workshops)
├── 1.6 CRUD Usuarios por taller

FASE 2 (Alta) - Semanas 2-3
├── 2.1 Status Logs (modelo + servicio)
├── 2.2 Integrar status_logs en WorkOrder updates
├── 2.3 Validaciones de unicidad (customer, vehicle)
├── 2.4 Validaciones de coherencia shop_id

FASE 3 (Media) - Semanas 3-4
├── 3.1 Paginación en todos los listados
├── 3.2 Filtros avanzados en WorkOrders
├── 3.3 Cálculo de totales por orden
├── 3.4 Búsquedas (LIKE)

FASE 4 (Baja) - Semana 4+
├── 4.1 Dashboard/stats
├── 4.2 Soft delete
└── 4.3 Exportación CSV/PDF
```

---

## 6. ESQUEMA DE TABLAS PENDIENTES

### Tabla: roles
```sql
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Tabla: user_roles
```sql
CREATE TABLE user_roles (
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    role_id INTEGER REFERENCES roles(id) ON DELETE CASCADE,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, role_id)
);
```

### Tabla: status_logs
```sql
CREATE TABLE status_logs (
    id SERIAL PRIMARY KEY,
    work_order_id INTEGER REFERENCES work_orders(id) ON DELETE CASCADE,
    old_status VARCHAR(50),
    new_status VARCHAR(50) NOT NULL,
    reason TEXT NOT NULL,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 7. PRÓXIMOS PASOS

1. **Confirmar fase inicial:** ¿Comenzamos con FASE 1 (Roles y Permisos)?
2. **Ajustar prioridades:** ¿Hay algún módulo que necesite ejecutarse antes?
3. **Recursos:** ¿Cuántos desarrolladores estarán disponibles?
4. **Timeline:** ¿Hay fecha objetivo para alguna funcionalidad específica?

---

*Documento generado automáticamente como parte del planning del proyecto.*