# API Documentation - Taller App Backend

> **Base URL:** `http://localhost:8000`
> **Authentication:** Bearer Token (JWT)

---

## 1. Autenticación

### Login
```http
POST /auth
Content-Type: application/x-www-form-urlencoded

username=tu_usuario&password=tu_password
```

**Response:**
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "exp": "2024-01-01T00:00:00Z",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@taller.com",
    "name": "Admin User",
    "shop_id": 1
  }
}
```

> **Nota:** Usar el `access_token` en el header `Authorization: Bearer <token>`

---

## 2. Clientes (Customers)

### Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/customers` | Crear cliente |
| GET | `/customers` | Listar clientes del taller |
| GET | `/customers/by_document/{document_id}` | Buscar por documento |
| GET | `/customers/by_id/{customer_id}` | Buscar por ID |
| GET | `/customers/{customer_id}/details` | Cliente con vehículos |
| PUT | `/customers/{customer_id}` | Actualizar cliente |

### Schemas

**CustomerCreate / CustomerUpdate:**
```json
{
  "document_id": "12345678",
  "name": "Juan",
  "last_name": "Pérez",
  "phone": "+56912345678",
  "email": "juan@email.com",
  "address": "Calle 123"
}
```

**CustomerRead:**
```json
{
  "id": 1,
  "shop_id": 1,
  "document_id": "12345678",
  "name": "Juan",
  "last_name": "Pérez",
  "phone": "+56912345678",
  "email": "juan@email.com",
  "address": "Calle 123",
  "created_at": "2024-01-01T00:00:00Z"
}
```

**CustomerReadDetail:**
```json
{
  "id": 1,
  "document_id": "12345678",
  "name": "Juan",
  "last_name": "Pérez",
  "phone": "+56912345678",
  "email": "juan@email.com",
  "address": "Calle 123",
  "created_at": "2024-01-01T00:00:00Z",
  "workshop": {
    "name": "Taller Central",
    "owner_name": "Pedro García",
    "phone": "+56900000000",
    "address": "Av. Principal 100"
  },
  "vehicles": [
    {
      "id": 1,
      "vehicle_type": "CAR",
      "plate": "ABC-123",
      "brand": "Toyota",
      "model": "Corolla",
      "year": 2020
    }
  ]
}
```

---

## 3. Vehículos (Vehicles)

### Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/vehicles` | Listar vehículos del taller |
| GET | `/vehicles/searchByPlate/{plate}` | Buscar por patente |
| GET | `/vehicles/searchById/{id}` | Buscar por ID |
| POST | `/vehicles` | Crear vehículo |
| GET | `/vehicles/{id}/workorders` | Órdenes del vehículo |
| PUT | `/vehicles/{id}` | Actualizar vehículo |

### Schemas

**CreateVehicle:**
```json
{
  "customer_id": 1,
  "vehicle_type": "CAR",
  "plate": "ABC-123",
  "brand": "Toyota",
  "model": "Corolla",
  "year": 2020,
  "photo_url": "https://..."
}
```

**VehicleRead:**
```json
{
  "id": 1,
  "shop_id": 1,
  "customer_id": 1,
  "vehicle_type": "CAR",
  "plate": "ABC-123",
  "brand": "Toyota",
  "model": "Corolla",
  "year": 2020,
  "photo_url": null,
  "created_at": "2024-01-01T00:00:00Z"
}
```

### Vehicle Types
- `CAR`
- `SUV`
- `VAN`
- `MINIVAN`
- `PICKUP`
- `TRUCK`
- `SKID_STEER`
- `MOTORCYCLE`

---

## 4. Órdenes de Trabajo (Work Orders)

### Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/workorders/` | Listar órdenes (opcional `?id=1`) |
| POST | `/workorders/` | Crear orden |
| PUT | `/workorders/{id}` | Actualizar orden |

### Schemas

**NewWorkOrder (con items opcionales):**
```json
{
  "vehicle_id": 1,
  "initial_diagnosis": "Fallo en motor",
  "labor_estimate": 50000,
  "parts_estimate": 150000,
  "status": "RECEIVED",
  "notes": "Cliente solicitó prioridad",
  "workorder_items": [
    {
      "item_type": "DIAGNOSIS",
      "description": "Diagnóstico inicial",
      "quantity": 1,
      "unit_cost": 0,
      "unit_price": 0,
      "before_photo_url": null,
      "after_photo_url": null
    },
    {
      "item_type": "LABOR",
      "description": "Cambio de aceite",
      "quantity": 1,
      "unit_cost": 10000,
      "unit_price": 20000,
      "before_photo_url": "workorder_items/before_wo1_20240101.jpg",
      "after_photo_url": "workorder_items/after_wo1_20240101.jpg"
    }
  ]
}
```

**WorkOrdersRead:**
```json
{
  "id": 1,
  "shop_id": 1,
  "vehicle_id": 1,
  "created_by_user_id": 1,
  "check_in_at": "2024-01-01T10:00:00Z",
  "check_out_at": null,
  "initial_diagnosis": "Fallo en motor",
  "labor_estimate": "50000.00",
  "parts_estimate": "150000.00",
  "status": "RECEIVED",
  "notes": "Cliente solicitó prioridad",
  "created_at": "2024-01-01T10:00:00Z"
}
```

### Work Order Status
- `RECEIVED` - Recibido
- `DIAGNOSIS` - En diagnóstico
- `WAITING_APPROVAL` - Esperando aprobación
- `APPROVED` - Aprobado
- `IN_PROGRESS` - En progreso
- `WAITING_PARTS` - Esperando repuestos
- `REPAIRED` - Reparado
- `READY_FOR_DELIVERY` - Listo para entrega
- `COMPLETED` - Completado
- `CANCELLED` - Cancelado

---

## 5. Ítems de Orden de Trabajo (Work Order Items)

### Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/workorderitem/` | Listar ítems (opcional `?workOrderId=1`) |
| GET | `/workorderitem/{id}` | Obtener ítem por ID |
| POST | `/workorderitem/` | Crear ítem (con imágenes opcionales) |
| PUT | `/workorderitem/{id}` | Actualizar ítem |
| DELETE | `/workorderitem/{id}` | Eliminar ítem |

### Crear Ítem con Imágenes (multipart/form-data)

**IMPORTANTE:** El endpoint de creación acepta `multipart/form-data` para enviar imágenes.

**Parámetros del form-data:**

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `work_order_id` | integer | ✅ | ID de la orden de trabajo |
| `item_type` | string | ✅ | DIAGNOSIS, LABOR, o PART |
| `description` | string | ✅ | Descripción del trabajo |
| `quantity` | integer | ❌ | Default: 1 |
| `unit_cost` | number | ❌ | Costo interno (default: 0) |
| `unit_price` | number | ❌ | Precio al cliente (default: 0) |
| `before_photo` | file | ❌ | Foto antes del trabajo (JPEG, PNG, WEBP, GIF, BMP) |
| `after_photo` | file | ❌ | Foto después del trabajo (JPEG, PNG, WEBP, GIF, BMP) |

**Ejemplo Flutter:**
```dart
var uri = Uri.parse('http://localhost:8000/workorderitem/');
var request = http.MultipartRequest('POST', uri);

// Headers
request.headers['Authorization'] = 'Bearer $token';

// Campos requeridos
request.fields['work_order_id'] = '1';
request.fields['item_type'] = 'LABOR';
request.fields['description'] = 'Cambio de aceite';
request.fields['quantity'] = '1';
request.fields['unit_cost'] = '15000';
request.fields['unit_price'] = '25000';

// Fotos opcionales
if (antesFile != null) {
  request.files.add(await http.MultipartFile.fromPath(
    'before_photo', 
    antesFile.path,
  ));
}

if (despuesFile != null) {
  request.files.add(await http.MultipartFile.fromPath(
    'after_photo', 
    despuesFile.path,
  ));
}

var response = await request.send();
```

**WorkOrderItemResponse:**
```json
{
  "id": 1,
  "work_order_id": 1,
  "item_type": "LABOR",
  "description": "Cambio de aceite",
  "quantity": 1,
  "unit_cost": "15000.00",
  "unit_price": "25000.00",
  "before_photo_url": "/media/workorder_items/before_wo1_20240101_abc12345.jpg",
  "after_photo_url": "/media/workorder_items/after_wo1_20240101_def67890.jpg",
  "created_at": "2024-01-01T10:00:00Z"
}
```

**Acceso a las imágenes:**
Las imágenes se almacenan en `/media/workorder_items/` y son accesibles públicamente:
```
http://localhost:8000/media/workorder_items/before_wo1_20240101_abc12345.jpg
```

### Item Types
- `DIAGNOSIS` - Diagnóstico
- `LABOR` - Mano de obra
- `PART` - Repuesto

---

## 6. Talleres (Workshops)

### Endpoints

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/workshops` | Listar talleres | ✅ |
| POST | `/workshops` | Crear taller | ADMIN |
| GET | `/workshops/{id}` | Obtener taller | ✅ |
| PUT | `/workshops/{id}` | Actualizar taller | ADMIN |
| DELETE | `/workshops/{id}` | Eliminar taller | ADMIN |

---

## 7. Usuarios (Users)

### Endpoints

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/workshops/{shop_id}/users` | Listar usuarios | ✅ |
| POST | `/workshops/{shop_id}/users` | Crear usuario | ADMIN |
| GET | `/workshops/{shop_id}/users/{id}` | Obtener usuario | ✅ |
| PUT | `/workshops/{shop_id}/users/{id}` | Actualizar usuario | ADMIN |
| DELETE | `/workshops/{shop_id}/users/{id}` | Eliminar usuario | ADMIN |
| PATCH | `/workshops/{shop_id}/users/{id}/active` | Activar/desactivar | ADMIN |
| GET | `/workshops/{shop_id}/users/{id}/roles` | Ver roles | ✅ |

### Schemas

**UserCreate:**
```json
{
  "username": "jsmith",
  "full_name": "Juan Smith",
  "email": "juan@email.com",
  "password": "securepassword123",
  "is_active": true
}
```

**UserUpdate:**
```json
{
  "username": "jsmith",
  "full_name": "Juan Smith",
  "email": "juan@email.com",
  "password": "newpassword123",
  "is_active": true
}
```

**UserRead:**
```json
{
  "id": 1,
  "shop_id": 1,
  "username": "jsmith",
  "full_name": "Juan Smith",
  "email": "juan@email.com",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z"
}
```

**UserReadWithRoles:**
```json
{
  "id": 1,
  "shop_id": 1,
  "username": "jsmith",
  "full_name": "Juan Smith",
  "email": "juan@email.com",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z",
  "roles": ["ADMIN", "MECHANIC"]
}
```

---

## 8. Roles

### Endpoints

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/roles` | Listar roles | ✅ |
| POST | `/roles` | Crear rol | ✅ |
| GET | `/roles/{id}` | Obtener rol | ✅ |
| PUT | `/roles/{id}` | Actualizar rol | ✅ |
| DELETE | `/roles/{id}` | Eliminar rol | ✅ |
| GET | `/roles/users/{user_id}/roles` | Roles de usuario | ✅ |
| POST | `/roles/users/{user_id}/roles` | Asignar rol | ✅ |
| DELETE | `/roles/users/{user_id}/roles/{role_id}` | Quitar rol | ✅ |

### Schemas

**RoleCreate:**
```json
{
  "name": "MECHANIC",
  "description": "Técnico mecánico del taller"
}
```

**RoleRead:**
```json
{
  "id": 1,
  "name": "MECHANIC",
  "description": "Técnico mecánico del taller",
  "created_at": "2024-01-01T00:00:00Z"
}
```

**UserRoleAssign:**
```json
{
  "role_id": 1
}
```

### Roles Disponibles
- `ADMIN` - Administrador del taller
- `MECHANIC` - Mecánico
- `VIEW_ONLY` - Solo lectura

---

## 9. Códigos de Error

| Código | Descripción |
|--------|-------------|
| 400 | Bad Request - Datos inválidos |
| 401 | No autenticado |
| 403 | Sin permisos suficientes |
| 404 | Recurso no encontrado |
| 409 | Conflicto (duplicado) |
| 422 | Error de validación |
| 500 | Error interno del servidor |

---

## 10. Notas Importantes

1. **Multi-tenant:** Todos los endpoints (excepto auth y roles globales) filtran automáticamente por `shop_id` del usuario autenticado.

2. **Autenticación:** El token JWT contiene `shop_id`, `username` e `id` del usuario.

3. **Autorización:** Los endpoints que modifican datos (POST, PUT, DELETE) requieren el rol `ADMIN`.

4. **Validaciones:**
   - Email y username deben ser únicos dentro de cada taller
   - La patente del vehículo debe ser única dentro del taller
   - El documento del cliente debe ser único dentro del taller
