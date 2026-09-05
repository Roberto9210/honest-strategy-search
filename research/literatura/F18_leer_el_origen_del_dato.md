# F18 — Antes de usar un conjunto de datos, leer su documentación de origen y anotar los cambios de formato, de fuente y de resolución que lo parten

**VENTANA L. NO MIDE NADA. K sigue en 261.**

> ## LA REGLA
>
> **Ningún conjunto de datos entra a una medición sin una FICHA DE ORIGEN escrita antes: de dónde viene,
> desde cuándo, con qué reloj, y en qué fechas cambió de formato, de fuente o de resolución. Los cortes
> se anotan como fechas, y cualquier comparación entre lados de un corte se declara como comparación
> entre dos datos, no entre dos épocas.**

---

# El caso que la descubrió

**`D19`, 2026-09-05.** La casa compró `mbo` y barras de un minuto del ES a Databento, reconstruyó con ellos
la cola FIFO, midió markouts, comparó 2017 con 2026 y encontró 10,6× más eventos de libro por día. **Nadie
había leído el catálogo del conjunto.** Cuando Roberto lo leyó, decía: desde marzo de 2017 el feed pasa de
profundidad agregada por precio a evento por orden; antes de 2017-05-21 los datos vienen de archivos
planos FIX sin sellos de captura; antes de 2015-11-20 la resolución es de milisegundo. **Tres cortes
adentro de una muestra de cuatro años, y dos de ellos en el medio de la comparación que se había hecho.**

**La autocrítica que la precede:** *la fuente de un dato comprado es lo primero que hay que leer y fue lo
último.* Nos alcanza a los tres.

# Por qué es una regla y no un recordatorio

Un corte de formato **produce diferencias que parecen de mercado**: más eventos, otro reloj, otra
profundidad. Y esas diferencias van **siempre en la dirección de "el mercado cambió"**, que es una
conclusión atractiva porque justifica no poder comparar. **Un corte no leído es una variable tratada
como constante (`A03`) con nombre y fecha.**

# La ficha de origen — qué tiene que tener

| campo | qué se anota |
|---|---|
| proveedor y conjunto | nombre exacto (`GLBX.MDP3`), esquema (`mbo`, `ohlcv-1m`…) |
| cobertura | fecha de inicio y fin **según el proveedor**, no según lo que se compró |
| **cortes de formato** | fechas en que el contenido cambia de naturaleza (agregado → por orden) |
| **cortes de fuente** | fechas en que el proveedor cambia de dónde saca el dato (captura propia → archivos del mercado) |
| **cortes de resolución** | fechas en que cambia el reloj (ms → ns) o el sello (con captura → sin captura) |
| reloj y sincronización | UTC, PTP, hardware; y **en qué zona horaria están las barras que usamos** |
| definición de sesión | qué día es "un día" para el proveedor (ETH, RTH, corte a las 17:00 CT) |
| simbología | continuo o contrato; regla de empalme y fechas de rollo |
| **qué mediciones de la casa cruzan cada corte** | la lista, para saber qué revisar |

# Aplicación retroactiva: los conjuntos que la casa ya usa

| conjunto | qué tiene | qué le falta |
|---|---|---|
| ES `ohlcv-1m` 2016-2019, Databento | verificado al tick contra NT8 en 828 barras (memoria de la casa) | **la ficha**: si las barras pre-2017-05 salen de FIX plano, ¿cambia algo en OHLCV? Probablemente no; **hay que leerlo, no suponerlo** |
| ES `mbo`, seis días | `mbo_lib.py` supone `order_id` real | **las seis fechas contra 2017-03 y 2017-05-21** (`D19`) |
| la caja, ES diario 2020-2026 | sellada | su ficha se escribe **ahora, sin abrirla**: proveedor, sesión, empalme. Lo que se puede saber del catálogo sin mirar el dato |
| 6E `tbbo` tres días, 6J/6E `ohlcv-1m` | sólo cotizados | ficha antes de comprar, no después |
| NT8 diarios | sesión ETH verificada | reloj y empalme de contrato, si no están escritos |

**`datos_crudos.md` de G existe y es el lugar natural de estas fichas. No lo toco: es territorio de G.
Lo que esta regla pide es que cada conjunto tenga la suya ahí antes del próximo uso.**

# Condición de falla de la regla

**Falla si leer el origen no cambia nunca una medición**: entonces es burocracia. **Ya cambió una** —la
comparación 2017-2026 tiene que rehacerse con fechas posteriores a mayo de 2017— **antes de estar
escrita.**

**Costos:** dinero cero, cartuchos cero, K en 261. Tiempo: el de leer un catálogo por conjunto, una vez.
