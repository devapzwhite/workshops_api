# Contexto funcional – API de gestión de talleres mecánicos

Esta API REST asíncrona está construida con FastAPI, SQLAlchemy async y PostgreSQL, y está diseñada para gestionar la operación diaria de uno o varios talleres mecánicos (shops).

El objetivo es centralizar:  
- Datos del taller y sus usuarios.  
- Clientes y sus vehículos por taller.  
- Órdenes de trabajo y el detalle de mano de obra, diagnósticos y repuestos.  
- Historial de estados de cada orden.  

Todo el diseño funcional que se describe aquí **debe respetar estrictamente** el esquema de base de datos actual (no inventar columnas ni tablas nuevas sin que el desarrollador lo indique explícitamente).

---

## 1. Modelo de dominio (visión general)

### 1.1 Talleres (workshops)

Tabla: `workshops`

Rol en el negocio: representa un taller mecánico independiente (multi-shop). Cada taller tiene:  
- `id`: identificador del taller.  
- `name`: nombre comercial del taller.  
- `owner_name`: nombre del dueño.  
- `phone`: teléfono de contacto.  
- `address`: dirección física.  
- `created_at`: fecha de creación del registro.  

Relaciones clave:  
- Un taller tiene muchos usuarios (`users`).  
- Un taller tiene muchos clientes (`customers`).  
- Un taller tiene muchos vehículos (`vehicles`).  
- Un taller tiene muchas órdenes de trabajo (`work_orders`).  

### 1.2 Usuarios, roles y autenticación

Tablas: `users`, `roles`, `user_roles`

#### Users
`users` representa a las personas que usan el sistema dentro de un taller:  
- `id`: identificador del usuario.  
- `shop_id`: referencia al taller (`workshops.id`). Un usuario siempre pertenece a un solo taller.  
- `username`: nombre de usuario único dentro del taller.  
- `full_name`: nombre completo.  
- `email`: correo, único dentro del taller.  
- `password`: hash de contraseña (nunca se expone en respuestas).  
- `is_active`: indica si el usuario puede autenticarse/usar el sistema.  
- `created_at`: fecha de creación.  

Restricciones importantes:  
- `UNIQUE (shop_id, email)`  
- `UNIQUE (shop_id, username)`  

Esto implica que el mismo email/username puede existir en otro taller distinto, pero no duplicarse dentro del mismo taller.

#### Roles
`roles` define los tipos de rol disponibles a nivel global:  
- `id`  
- `name`: valores como `'ADMIN'`, `'MECHANIC'`, `'VIEW_ONLY'`, etc. (único).  
- `description`: descripción funcional del rol.  

#### User_roles
`user_roles` es la tabla de unión muchos-a-muchos entre `users` y `roles`:  
- `user_id` → `users.id`  
- `role_id` → `roles.id`  
- PK compuesta (`user_id`, `role_id`).  

A nivel funcional:  
- Un usuario puede tener uno o varios roles.  
- Los roles se usan para controlar qué endpoints puede usar cada usuario (autorización por rol).

> Nota: la lógica de autenticación/autorización (JWT, OAuth2, etc.) debe construirse respetando este modelo. El sistema puede asumir un esquema típico de login por `username` o `email` dentro de un `shop_id`, pero siempre usando `password` hasheado.

---

## 2. Clientes y vehículos

### 2.1 Clientes (customers)

Tabla: `customers`

Representa a los clientes del taller (propietarios de vehículos).  
- `id`  
- `shop_id`: taller al que pertenece el cliente.  
- `document_id`: RUT/DNI u otro identificador oficial.  
- `name`: nombre(s).  
- `last_name`: apellido(s).  
- `phone`, `email`, `address`.  
- `created_at`.  

Regla de unicidad:  
- `UNIQUE (shop_id, document_id)` → un mismo documento no se repite dentro del mismo taller.  

Consideraciones funcionales:  
- Un mismo cliente (misma persona) podría existir en más de un taller si se registró en cada uno por separado.  
- Los endpoints deben siempre filtrar por `shop_id` para que un taller nunca vea clientes de otro.

### 2.2 Vehículos (vehicles)

Tabla: `vehicles`

Representa los vehículos atendidos en el taller. Cada vehículo está asociado a un cliente específico del taller.  
- `id`  
- `shop_id`: taller propietario del registro.  
- `customer_id`: referencia a `customers.id`.  
- `vehicle_type`: enumeración controlada con los valores:  
  - `'CAR'`  
  - `'SUV'`  
  - `'VAN'`  
  - `'PICKUP'`  
  - `'TRUCK'`  
  - `'SKID_STEER'`  
  - `'MOTORCYCLE'`  
- `plate`: patente/placa.  
- `brand`: marca.  
- `model`: modelo.  
- `year`: año de fabricación.  
- `photo_url`: URL opcional de foto del vehículo.  
- `created_at`.  

Regla de unicidad:  
- `UNIQUE (shop_id, plate)` → la misma placa no puede estar duplicada dentro del mismo taller.  

Relaciones funcionales:  
- Un cliente puede tener muchos vehículos.  
- Un vehículo puede tener muchas órdenes de trabajo (`work_orders`).  

---

## 3. Órdenes de trabajo

### 3.1 work_orders

Tabla: `work_orders`

Una orden de trabajo representa el proceso de atención de un vehículo, desde el ingreso al taller hasta la entrega.  
Campos:  
- `id`  
- `shop_id`: taller que gestiona la orden.  
- `vehicle_id`: referencia al vehículo (`vehicles.id`).  
- `created_by_user_id`: usuario que creó la orden (`users.id`).  
- `check_in_at`: fecha/hora de ingreso del vehículo (por defecto `CURRENT_TIMESTAMP`).  
- `check_out_at`: fecha/hora de salida del vehículo (se establece al finalizar/entregar).  
- `initial_diagnosis`: descripción del problema inicial o diagnóstico preliminar.  
- `labor_estimate`: estimación de mano de obra (monto).  
- `parts_estimate`: estimación de repuestos (monto).  
- `status`: estado actual de la orden.  
- `notes`: notas internas o generales.  
- `created_at`.  

Estados posibles (`status`):  
- `'RECEIVED'`  
- `'DIAGNOSIS'`  
- `'WAITING_APPROVAL'`  
- `'APPROVED'`  
- `'IN_PROGRESS'`  
- `'WAITING_PARTS'`  
- `'REPAIRED'`  
- `'READY_FOR_DELIVERY'`  
- `'COMPLETED'`  
- `'CANCELLED'`  

Interpretación funcional típica de los estados:  
- `RECEIVED`: el vehículo fue recibido, se abre la orden.  
- `DIAGNOSIS`: se está realizando diagnóstico o revisión.  
- `WAITING_APPROVAL`: se envió presupuesto al cliente, esperando su autorización.  
- `APPROVED`: el cliente aprobó el trabajo.  
- `IN_PROGRESS`: el vehículo está en reparación.  
- `WAITING_PARTS`: trabajo pausado a la espera de repuestos.  
- `REPAIRED`: trabajo de reparación finalizado.  
- `READY_FOR_DELIVERY`: vehículo listo para entrega.  
- `COMPLETED`: orden cerrada, vehículo entregado y facturación (si aplica) completada.  
- `CANCELLED`: orden cancelada (por cliente o taller).  

Reglas de negocio sugeridas:  
- `shop_id` de la orden siempre debe coincidir con el `shop_id` del vehículo.  
- No se permite cambiar el vehículo de una orden una vez creada, salvo lógica explícita.  
- Cambios de `status` deben registrarse en la tabla `status_logs`.

---

## 4. Ítems de la orden (mano de obra, diagnóstico, partes)

### 4.1 work_order_items

Tabla: `work_order_items`

Representa cada línea de detalle asociada a una orden de trabajo.  
Campos:  
- `id`  
- `work_order_id`: referencia a `work_orders.id`.  
- `item_type`:  
  - `'DIAGNOSIS'`: actividades de diagnóstico (podrían o no ser cobradas).  
  - `'LABOR'`: horas de mano de obra / tareas específicas.  
  - `'PART'`: repuestos o materiales.  
- `description`: descripción del trabajo o repuesto.  
- `quantity`: cantidad (entero).  
- `unit_cost`: costo interno para el taller (para cálculo de margen).  
- `unit_price`: precio cobrado al cliente por unidad.  
- `before_photo_url`: foto antes del trabajo (opcional).  
- `after_photo_url`: foto después del trabajo (opcional).  
- `created_at`.  

Reglas funcionales típicas:  
- El total de un ítem se calcula como `quantity * unit_price`.  
- El costo total interno de un ítem se calcula como `quantity * unit_cost`.  
- El backend puede exponer totales calculados a partir de los ítems para una orden dada (sumatorias por tipo o totales generales).  

---

## 5. Historial de estados

### 5.1 status_logs

Tabla: `status_logs`

Registra la trazabilidad de los cambios de estado de una orden de trabajo.  
Campos:  
- `id`  
- `work_order_id`: referencia a `work_orders.id`.  
- `old_status`: estado anterior (puede ser `NULL` si es el primer estado, según la lógica que se implemente).  
- `new_status`: nuevo estado, **obligatorio**.  
- `reason`: motivo del cambio de estado (texto obligatorio).  
- `changed_at`: fecha/hora del cambio (`DEFAULT CURRENT_TIMESTAMP`).  

Reglas de negocio recomendadas:  
- Cada vez que cambie `work_orders.status`, se debe crear un registro en `status_logs`.  
- `old_status` debe coincidir con el estado previo real de la orden; `new_status` con el nuevo estado.  
- `reason` sirve tanto para auditoría interna como para mostrar un historial al usuario final (por ejemplo, “Cliente aprobó presupuesto por teléfono”).  

---

## 6. Consideraciones generales para los endpoints

Estas pautas son para guiar a cualquier IA o desarrollador al momento de crear/editar endpoints, servicios y esquemas.

### 6.1 Multi-taller (multi-tenant sencillo)

- Casi todas las entidades están asociadas a `shop_id`.  
- Los endpoints deben estar diseñados para que un usuario autenticado opere únicamente sobre los datos de su `shop_id`.  
- Nunca se debe permitir que un usuario de un taller liste, lea o modifique datos de otro taller.  

### 6.2 Validaciones mínimas por entidad

Al crear o actualizar registros, deben respetarse como mínimo las siguientes validaciones:

- `workshops`  
  - `name` obligatorio.  

- `users`  
  - `shop_id` obligatorio y debe existir.  
  - `username`, `full_name`, `email`, `password` obligatorios.  
  - Respeto de las restricciones `UNIQUE (shop_id, email)` y `UNIQUE (shop_id, username)`.  
  - No exponer `password` en respuestas.  

- `customers`  
  - `shop_id` obligatorio y existente.  
  - `document_id`, `name`, `last_name` obligatorios.  
  - Cumplir `UNIQUE (shop_id, document_id)`.  

- `vehicles`  
  - `shop_id` obligatorio y coherente con el `shop_id` del `customer`.  
  - `customer_id` debe existir.  
  - `vehicle_type` debe estar dentro del conjunto permitido.  
  - `plate`, `brand`, `model` obligatorios.  
  - Cumplir `UNIQUE (shop_id, plate)`.  

- `work_orders`  
  - `shop_id` obligatorio y coherente con el `vehicle`.  
  - `vehicle_id` obligatorio y existente.  
  - `status` debe ser uno de los valores permitidos.  

- `work_order_items`  
  - `work_order_id` obligatorio y existente.  
  - `item_type` en el conjunto permitido.  
  - `description` obligatorio.  
  - `quantity` ≥ 1.  

- `status_logs`  
  - `work_order_id` obligatorio y existente.  
  - `new_status` obligatorio y en el conjunto permitido.  
  - `reason` obligatorio.  

### 6.3 Buenas prácticas sugeridas para la API

- Usar respuestas paginadas para listados extensos (clientes, vehículos, órdenes).  
- Exponer filtros por `status`, `vehicle_id`, `customer_id`, rangos de fechas (`check_in_at`, `check_out_at`).  
- Ocultar siempre campos sensibles (`password`, datos internos de costos si se decide no exponerlos al front).  
- Mantener consistencia en nombres de rutas, por ejemplo:  
  - `/shops`  
  - `/shops/{shop_id}/users`  
  - `/shops/{shop_id}/customers`  
  - `/shops/{shop_id}/vehicles`  
  - `/shops/{shop_id}/work-orders`  
  - `/shops/{shop_id}/work-orders/{work_order_id}/items`  
  - `/shops/{shop_id}/work-orders/{work_order_id}/status-logs`  

---

## 7. Uso de este documento por IA

Cuando uses una IA para generar nuevos endpoints o servicios en este backend:

1. Respeta el esquema de tablas y columnas aquí descrito, sin crear nuevas columnas/tablas a menos que el desarrollador lo pida explícitamente.  
2. Cualquier campo calculado (totales, resúmenes, etc.) debe generarse a nivel de lógica de negocio o respuesta, **no** como cambios en el esquema.  
3. Antes de proponer migraciones, verifica que no se rompa la compatibilidad con este modelo de dominio.  
4. Mantén la separación clara entre:
   - Lógica de autenticación/autorización (basada en `users`, `roles`, `user_roles`).  
   - Lógica de negocio del taller (clientes, vehículos, órdenes, ítems y status logs).  
