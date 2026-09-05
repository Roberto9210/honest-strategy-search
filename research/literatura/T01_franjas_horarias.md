# T01 — En qué franja horaria vive cada sobreviviente. Para aplicar el perfil en diez minutos.

**VENTANA L. NO MIDE CANDIDATAS; corre CONTROLES DEL INSTRUMENTO desde el 2026-09-05 (rol ampliado por Roberto, ver `INDICE`). K sigue en 261.**

> ## EL RANKING ESTÁ CONGELADO
>
> Instrucción de Roberto del 2026-09-05: **no recalcular, no reordenar, no promover ni bajar a nadie**
> hasta que la VENTANA G mida el perfil de volatilidad intradiaria. Los cinco márgenes salen del mismo
> escalado uniforme y cualquier trabajo de ranking ahora se tira.
>
> **Lo único que este documento hace es dejar preparada la corrección**: cuando llegue el perfil, la
> fracción de varianza de cada franja reemplaza al `√(T/T_día)` y los cinco márgenes se recalculan en
> diez minutos.
>
> **Actualización del mismo día:** el perfil del ES **ya está en el repo** (VENTANA G, commit
> `7461919`). **Roberto mantiene el congelamiento**, y el perfil corrige sólo a **tres** de las cinco:
> L07 y L08 viven en otros mercados. Ver [T02](T02_L07_L08_medicion_que_nadie_puede_hacer.md).

---

# La tabla

| candidata | ventana | franja horaria, hora del este | mercado | **pico o valle** | lo que ya sabemos |
|---|---|---|---|---|---|
| **L01** | última media hora de la sesión de contado | **15:30 – 16:00** | ES | **PICO de la tarde** | Baltussen implica ~25 pb para esta media hora (cartera 1/N de índices, 1974-2020). **G midió 20,92 pb en el ES 2016-2019: factor 1,81** sobre la raíz del tiempo. Ver [A05](A05_control_externo_baltussen.md) |
| **L03** | los 30 minutos antes de la publicación de las 10:00 | **09:30 – 10:00** | ES | **PICO de la mañana, el más alto del día** | es la primera media hora de la sesión de contado, y Kurov et al. reportan que el volumen se multiplica por más de cinco a las 9:30 |
| **L10**, versión de una hora | última hora antes del cierre | **15:00 – 16:00** | ES | **PICO de la tarde** | comparte franja con L01; `D09` estimó 17,5 % de la varianza diaria en esta hora, **FRÁGIL** |
| **L07** | de 5 minutos antes a 5 minutos después del fixing de Tokio | **00:50 – 01:00 GMT** = **19:50 – 20:00** del este del día anterior | USD/JPY, 6J | **PICO local de SU mercado** | es un pico de volumen documentado por Ito y Yamada. **La U del ES no aplica**: es otro instrumento y otra sesión |
| **L08** | la hora previa al fixing de Londres | **15:00 – 16:00 Londres** = **10:00 – 11:00** del este en invierno | divisas mayores, 6E | **PICO del día de divisas** | es el solapamiento Londres–Nueva York, el tramo de mayor volumen del mercado cambiario. **La U del ES no aplica** |

## Lo que salta de la tabla, y hay que decirlo sin sacar conclusiones de ranking

**Los cinco viven en picos. Ninguno vive en un valle.** Eso no es casualidad: los mecanismos que la
literatura documenta son flujos —rebalanceo, cobertura, órdenes de clientes, publicaciones— y los
flujos se concentran donde hay volumen. *(Observación sobre cinco casos, no una ley. **Falla** en
cuanto una candidata con flujo documentado viva en un valle; la primera la anula. Ver `A06`.)*

> **Consecuencia para la corrección pendiente: el escalado uniforme SUBESTIMÓ el ruido de los cinco, y
> los cinco márgenes van a BAJAR cuando llegue el perfil.** La única pregunta abierta es **cuánto cada
> uno**, y eso decide el orden. **No se adelanta.**
> *(Para L01, L03 y L10 ya bajaron: `D13`. Para L07 y L08 es una predicción sin medir: **falla** si el
> desvío medido de su ventana resulta menor que el del escalado uniforme, 4,7 y 11,4 pb. Ver `A06`.)*

**Veredictos absolutos con el perfil, sin orden:** [D13](D13_veredictos_absolutos.md).

## Qué perfil hace falta, exactamente, para que la corrección sea de diez minutos

| para | hace falta |
|---|---|
| L01, L03, L10 | **la fracción de la varianza de cierre a cierre del ES que cae en cada media hora de la sesión de contado**, 2016-2019. Una tabla de trece filas. **Es lo que la VENTANA G tiene pedido** |
| L07 | la fracción de la varianza diaria de USD/JPY en la ventana 00:50-01:00 GMT. **Requiere los datos de 6J, que no se compraron** |
| L08 | la fracción de la varianza diaria de una moneda mayor en la hora previa a las 16:00 de Londres. **Requiere los datos de 6E, que no se compraron** |

**Las tres del ES se corrigen con una sola medición que ya está pedida. Las dos de divisas esperan
una decisión de compra que no es mía.**
