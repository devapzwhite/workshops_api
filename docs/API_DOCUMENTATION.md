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

---

## 3. Vehículos (Vehicles)

### Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/vehicles` | Listar vehículos del taller |
| GET | `/vehicles/searchByPlate/{plate}` | Buscar por patente |
| POST | `/vehicles` | Crear vehículo |
| GET | `/vehicles/{id}/workorders` | Órdenes del vehículo |
| PUT | `/vehicles/{id}` | Actualizar vehículo |

### Vehicle Types
- `CAR`, `SUV`, `VAN`, `MINIVAN`, `PICKUP`, `TRUCK`, `SKID_STEER`, `MOTORCYCLE`

---

## 4. Órdenes de Trabajo (Work Orders)

### Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/workorders/` | Listar órdenes (opcional `?id=1`) |
| POST | `/workorders/` | Crear orden |
| PUT | `/workorders/{id}` | Actualizar orden |

### Work Order Status
- `RECEIVED`, `DIAGNOSIS`, `WAITING_APPROVAL`, `APPROVED`, `IN_PROGRESS`, `WAITING_PARTS`, `REPAIRED`, `READY_FOR_DELIVERY`, `COMPLETED`, `CANCELLED`

---

## 5. Ítems de Orden de Trabajo (Work Order Items)

### Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/workorderitem/` | Listar ítems (opcional `?workOrderId=1`) |
| GET | `/workorderitem/{id}` | Obtener ítem por ID |
| POST | `/workorderitem/` | Crear ítem (con imágenes) |
| PUT | `/workorderitem/{id}` | Actualizar ítem |
| DELETE | `/workorderitem/{id}` | Eliminar ítem |

---

### Crear Ítem con Imágenes (multipart/form-data)

**URL:** `POST http://localhost:8000/workorderitem/`

**Tipo de Body:** `multipart/form-data`

**Parámetros del form-data:**

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `workorderid` | integer | ✅ | ID de la orden de trabajo |
| `itemtype` | string | ✅ | DIAGNOSIS, LABOR, o PART |
| `description` | string | ✅ | Descripción del trabajo |
| `quantity` | integer | ❌ | Default: 1 |
| `unitcost` | number | ❌ | Costo interno (default: 0) |
| `unitprice` | number | ❌ | Precio al cliente (default: 0) |
| `beforephoto` | file | ❌ | Foto antes del trabajo (image/*) |
| `afterphoto` | file | ❌ | Foto después del trabajo (image/*) |

**Ejemplo Flutter:**
```dart
import 'dart:io';
import 'package:http/http.dart' as http;

Future<void> createWorkOrderItem({
  required String token,
  required int workOrderId,
  required String itemType,
  required String description,
  File? beforePhoto,
  File? afterPhoto,
}) async {
  var uri = Uri.parse('http://localhost:8000/workorderitem/');
  var request = http.MultipartRequest('POST', uri);

  // Headers
  request.headers['Authorization'] = 'Bearer $token';

  // Campos requeridos
  request.fields['workorderid'] = workOrderId.toString();
  request.fields['itemtype'] = itemType;  // 'DIAGNOSIS', 'LABOR', o 'PART'
  request.fields['description'] = description;

  // Campos opcionales
  request.fields['quantity'] = '1';
  request.fields['unitcost'] = '15000';
  request.fields['unitprice'] = '25000';

  // Fotos opcionales (antes)
  if (beforePhoto != null) {
    request.files.add(await http.MultipartFile.fromPath(
      'beforephoto',
      beforePhoto.path,
    ));
  }

  // Fotos opcionales (después)
  if (afterPhoto != null) {
    request.files.add(await http.MultipartFile.fromPath(
      'afterphoto',
      afterPhoto.path,
    ));
  }

  var response = await request.send();
  
  if (response.statusCode == 201) {
    var responseData = await response.stream.bytesToString();
    print('Ítem creado: $responseData');
  } else {
    print('Error: ${response.statusCode}');
  }
}

// Uso:
await createWorkOrderItem(
  token: 'tu_token_jwt',
  workOrderId: 1,
  itemType: 'LABOR',
  description: 'Cambio de aceite',
  beforePhoto: File('/path/antes.jpg'),
  afterPhoto: File('/path/despues.jpg'),
);
```

**Response (201 Created):**
```json
{
  "id": 1,
  "work_order_id": 1,
  "item_type": "LABOR",
  "description": "Cambio de aceite",
  "quantity": 1,
  "unit_cost": "15000.00",
  "unit_price": "25000.00",
  "before_photo_url": "workorder_items/before_wo1_20240101_abc12345.jpg",
  "after_photo_url": "workorder_items/after_wo1_20240101_def67890.jpg",
  "created_at": "2024-01-01T10:00:00Z"
}
```

**Acceso a las imágenes (PROTEGIDO):**
Las imágenes ahora requieren autenticación JWT. El endpoint verifica que el usuario pertenece al mismo taller (shop_id) de la orden de trabajo.

```
GET http://localhost:8000/media/workorder_items/before_wo1_20240101_abc12345.jpg
Headers: Authorization: Bearer <token>
```

### Item Types
- `DIAGNOSIS` - Diagnóstico
- `LABOR` - Mano de obra
- `PART` - Repuesto

---

## 6. Talleres (Workshops)

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/workshops` | Listar talleres | ✅ |
| POST | `/workshops` | Crear taller | ADMIN |
| GET | `/workshops/{id}` | Obtener taller | ✅ |
| PUT | `/workshops/{id}` | Actualizar taller | ADMIN |
| DELETE | `/workshops/{id}` | Eliminar taller | ADMIN |

---

## 7. Usuarios (Users)

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/workshops/{shop_id}/users` | Listar usuarios | ✅ |
| POST | `/workshops/{shop_id}/users` | Crear usuario | ADMIN |
| GET | `/workshops/{shop_id}/users/{id}` | Obtener usuario | ✅ |
| PUT | `/workshops/{shop_id}/users/{id}` | Actualizar usuario | ADMIN |
| DELETE | `/workshops/{shop_id}/users/{id}` | Eliminar usuario | ADMIN |
| PATCH | `/workshops/{shop_id}/users/{id}/active` | Activar/desactivar | ADMIN |

---

## 8. Roles

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

1. **Multi-tenant:** Todos los endpoints filtran automáticamente por `shop_id` del usuario autenticado.

2. **Autenticación:** El token JWT contiene `shop_id`, `username` e `id` del usuario.

3. **Endpoints que requieren ADMIN:** POST, PUT, DELETE en talleres, usuarios.

4. **Imágenes protegidas:** Las imágenes de WorkOrderItem ahora requieren autenticación JWT. Ver sección 5.1.

---

## 5.1 Imágenes de WorkOrderItem (Protegidas)

### Importante
Las imágenes de WorkOrderItem **ya no son públicas**. Requieren autenticación JWT y verificación de permisos por `shop_id`.

### Endpoint
```
GET /media/workorder_items/{filename}
```

### Encabezados requeridos
```
Authorization: Bearer <tu_token_jwt>
```

### Cómo obtener la URL de la imagen
Al crear un WorkOrderItem, la respuesta incluye los campos:
```json
{
  "before_photo_url": "workorder_items/before_wo1_20240101_abc12345.jpg",
  "after_photo_url": "workorder_items/after_wo1_20240101_def67890.jpg"
}
```

Debes prependear la base URL:
```dart
String baseUrl = 'http://localhost:8000';
String beforeImageUrl = '$baseUrl/media/${workOrderItem.before_photo_url}';
String afterImageUrl = '$baseUrl/media/${workOrderItem.after_photo_url}';
```

### Ejemplo completo en Flutter
```dart
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:flutter/material.dart';

class ImageService {
  final String baseUrl = 'http://localhost:8000';
  
  // Descargar imagen con autenticación
  Future<Image> loadProtectedImage(String? photoUrl, String token) async {
    if (photoUrl == null || photoUrl.isEmpty) {
      return Image.asset('assets/no_image.png');
    }
    
    String fullUrl = '$baseUrl/media/$photoUrl';
    
    // Usar con autenticación
    return Image.network(
      fullUrl,
      headers: {'Authorization': 'Bearer $token'},
      loadingBuilder: (context, child, loadingProgress) {
        if (loadingProgress == null) return child;
        return CircularProgressIndicator();
      },
      errorBuilder: (context, error, stackTrace) {
        return Icon(Icons.broken_image, size: 50);
      },
    );
  }
  
  // Obtener bytes de imagen (útil para caching)
  Future<List<int>?> getImageBytes(String? photoUrl, String token) async {
    if (photoUrl == null || photoUrl.isEmpty) return null;
    
    String fullUrl = '$baseUrl/media/$photoUrl';
    var response = await http.get(
      Uri.parse(fullUrl),
      headers: {'Authorization': 'Bearer $token'},
    );
    
    if (response.statusCode == 200) {
      return response.bodyBytes;
    }
    return null;
  }
}

// Widget de ejemplo
class WorkOrderItemImage extends StatelessWidget {
  final String? photoUrl;
  final String token;
  
  @override
  Widget build(BuildContext context) {
    if (photoUrl == null || photoUrl!.isEmpty) {
      return Icon(Icons.image_not_supported, size: 50);
    }
    
    String fullUrl = 'http://localhost:8000/media/$photoUrl';
    
    return Image.network(
      fullUrl,
      headers: {'Authorization': 'Bearer $token'},
    );
  }
}
```

### Códigos de respuesta
| Código | Descripción |
|--------|-------------|
| 200 | Imagen encontrada y devuelta |
| 401 | No autenticado (token inválido o ausente) |
| 404 | Imagen no encontrada o sin acceso |

### Seguridad
- El endpoint verifica que `WorkOrderItem` pertenezca a una `WorkOrder` con el mismo `shop_id` que el usuario autenticado.
- Si el usuario intenta acceder a una imagen de otro taller, recibe 404 (no 403) para no revelar la existencia del recurso.

---

## 5.2 Limpieza de Imágenes Huérfanas

### Endpoint
```
POST /media/cleanup-orphans
```

### Descripción
Elimina imágenes del filesystem que no están referenciadas en la base de datos. Útil para limpiar fotos antiguas que quedaron huérfanas por eliminaciones directas en BD u otros motivos.

### Encabezados requeridos
```
Authorization: Bearer <tu_token_jwt>
```

### Ejemplo de request
```bash
curl -X POST "http://localhost:8000/api/v1/media/cleanup-orphans" \
     -H "Authorization: Bearer <tu_token_jwt>"
```

### Response (200 OK)
```json
{
  "message": "Se eliminaron 5 imágenes huérfanas",
  "deleted_count": 5,
  "deleted_files": [
    "workorder_items/before_wo1_20240101_abc12345.jpg",
    "workorder_items/after_wo2_20240102_def67890.jpg"
  ],
  "total_orphans_found": 5
}
```

### Cómo funciona
1. Obtiene todas las URLs de fotos (`before_photo_url` y `after_photo_url`) almacenadas en la tabla `work_order_items`
2. Escanea el directorio `media/workorder_items/` en el filesystem
3. Compara los archivos físicos con las URLs de la BD
4. Elimina los archivos que no tienen referencia en la BD

### Cuándo usar este endpoint
- Después de migraciones o eliminaciones masivas
- Periódicamente como mantenimiento preventivo
- Cuando se detecten archivos sin uso en el directorio

### Códigos de respuesta
| Código | Descripción |
|--------|-------------|
| 200 | Limpieza completada exitosamente |
| 401 | No autenticado |
