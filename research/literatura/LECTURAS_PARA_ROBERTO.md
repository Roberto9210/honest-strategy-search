# LECTURAS PARA ROBERTO — lo que a esta ventana le rebotó, con qué buscar en cada una

**VENTANA L. NO MIDE NADA. K sigue en 261.** Roberto puede leer páginas que a mí me devuelven 403 o
binario. **Para cada ítem: qué es, dónde, qué extraer exactamente, y a qué documento alimenta.** Con
esto `INVENTARIO_2` y `D18` dejan de tener el límite declarado.

**Orden: por lo que puede cambiar un veredicto.**

| # | qué | dónde | **qué extraer, textual** | alimenta |
|---|---|---|---|---|
| **1** | **Búsqueda, no un paper:** *"E-mini S&P 500 intraday return predictability"* y *"index futures 5-minute momentum reversal"*, 2015-2025 | SSRN, Google Scholar | **títulos y resúmenes** de todo lo que mire el ES a horizontes de **1 a 30 minutos** con **≥ 5 señales por día**. Tanto hallazgos como nulos. Es lo único que puede convertir el cero de `INVENTARIO_2` en una candidata o confirmarlo como (B) | `INVENTARIO_2`, `D18` §5 |
| **2** | Baron, Brogaard, Hagströmer y Kirilenko 2019, *"Risk and Return in High-Frequency Trading"*, *JFQA* 54(3) | SSRN 2433118 (403 para mí) | instrumento y período (¿E-mini 2010-2012?); número de firmas de alta frecuencia; **ganancia por contrato**, separada en agresiva y pasiva; **concentración entre las más rápidas**; tenencia típica | `INVENTARIO_2` clase 3, `D17` §3, `D12` |
| 3 | Chordia, Roll y Subrahmanyam 2005, *"Evidence on the speed of convergence to market efficiency"*, *JFE* 76 | SSRN o la web de los autores | **el horizonte en minutos** al que la predictibilidad por desbalance de órdenes desaparece (¿5, 10, 30, 60?), y **cómo cambió** entre 1993 y 2002 | `D18` §2 |
| 4 | Chordia, Roll y Subrahmanyam 2008, *"Liquidity and market efficiency"*, *JFE* 87 | idem | la tendencia de la predictibilidad a 5 minutos a lo largo de las décadas; la relación con la liquidez | `D18` §2 |
| 5 | Brogaard, Hendershott y Riordan 2014, *"High-Frequency Trading and Price Discovery"*, *RFS* 27 | SSRN 1928510 | **el horizonte en segundos** al que las operaciones de alta frecuencia predicen el precio; la frase sobre "permanentes" y "transitorios" | `D18` §2, `D11` |
| 6 | Menkveld 2013, *"High frequency trading and the new market makers"*, *J. Financial Markets* | SSRN 1722924 | **ganancia bruta por operación** del creador de mercado de alta frecuencia, y su Sharpe si lo reporta | `D17` §3, la fila de Virtu |
| 7 | Prospecto de salida a bolsa de Virtu Financial, 2014 (formulario S-1) | sec.gov, EDGAR | la frase sobre **días perdedores** (recuerdo "uno en 1.238"): confirmar o corregir | `D17` §3 |
| 8 | Catálogo de Databento, conjunto `GLBX.MDP3` | databento.com/catalog/cme/GLBX.MDP3 (a mí me devolvió sólo la palabra "Databento") | **fecha de inicio de la cobertura** (¿2010-06?) y esquemas disponibles | `D14` §2, marcado FRÁGIL |
| 9 | CME Group, *Market Depth FAQ* (PDF) | cmegroup.com/market-data (ECONNRESET dos veces) | **cuántos niveles** por producto, y **desde cuándo** el E-mini publica diez | `D10` §(a) |
| 10 | Easley, López de Prado y O'Hara 2012, *"Flow toxicity and liquidity in a high-frequency world"*, *RFS* | SSRN 1695041 | sólo esto: **¿reportan alguna predictibilidad DIRECCIONAL?** Si no, la clase 6 queda como está | `INVENTARIO_2` clase 6 |

---

# ESTADO — 2026-09-05, después de la primera vuelta de Roberto

**Seis salieron, cinco bloqueadas.** Y una que no estaba en la lista contestó la pregunta de `D18`
mejor que las que sí estaban: **Boyarchenko, Larsen y Whelan, "The Overnight Drift", NY Fed SR 917**
→ `L12` y `D18` §1b.

| # | ítem | resultado |
|---|---|---|
| 1 | la búsqueda ES 1-30 min | **trajo BLW (horaria, 1/día) y dos nulos parciales** (Breedon-Ranaldo 2013; Yamamoto 2012). Nada a 1-30 min con ≥ 5/día |
| 2 | Baron et al. 2019 | **BLOQUEADO**, SSRN |
| 3, 4 | Chordia-Roll-Subrahmanyam 2005, 2008 | **BLOQUEADOS**, SSRN |
| 5 | Brogaard-Hendershott-Riordan 2014 | **BLOQUEADO**, SSRN |
| 6 | Menkveld 2013 | **BLOQUEADO**, SSRN |
| 7 | S-1 de Virtu | **LEÍDO**: un día perdedor en 1.238; el S-1 no dice "Sharpe" → `D17` corregido |
| 8 | catálogo Databento | **LEÍDO**: desde 2010-06-06; MBP-10; y el cambio de formato de marzo de 2017 → `D14`, `D10`, `D19` |
| 9 | FAQ de profundidad del CME | sin reportar |
| 10 | VPIN | **BLOQUEADO**, SSRN |

**Sobre los bloqueos, en las palabras de Roberto, para que quede escrito así y no como "no encontrado":**
*SSRN devuelve la misma verificación anti-bot que a esta ventana. No la rodea: eso está fuera de lo que
hace.* **Los cinco quedan como NO ACCESIBLES POR SSRN, no como no existentes.**

# SEGUNDA VUELTA — la frase exacta que hace falta de cada bloqueado, y dónde suelen alojarlo los autores

| # | paper | **la frase que necesito, y de qué sección** | dónde buscar la versión publicada o del autor |
|---|---|---|---|
| 2 | **Baron, Brogaard, Hagströmer y Kirilenko 2019**, *JFQA* | **(i)** en el resumen o la introducción: la frase con la **ganancia por contrato** de los de alta frecuencia, si separa **agresivos** de **pasivos**; **(ii)** en la sección de resultados sobre latencia: la frase que dice que **los más rápidos ganan más** (buscar "fastest" o "latency"); **(iii)** en la sección de datos: **instrumento y período** exactos (buscar "E-mini" y "August 2010") | página de Brogaard (Universidad de Utah, antes Washington); página de Hagströmer (Stockholm Business School); Kirilenko (Cambridge Judge) |
| 5 | **Brogaard, Hendershott y Riordan 2014**, *RFS* | **(i)** la frase del resumen: *"HFTs trade in the direction of permanent price changes and in the opposite direction of transitory pricing errors"* o como diga; **(ii)** cualquier frase que dé **el horizonte en segundos** al que las operaciones de alta frecuencia predicen el precio (buscar "seconds" en la sección del modelo de estado o en las tablas de retornos futuros) | página de Hendershott en Berkeley Haas: el archivo suele llamarse `HFT-PriceDiscovery.pdf`; página de Riordan |
| 6 | **Menkveld 2013**, *J. Financial Markets* | **(i)** la frase con la **ganancia bruta por operación** del creador de mercado de alta frecuencia (buscar "per trade" o "gross profit"); **(ii)** si aparece, su **Sharpe**; **(iii)** la muestra (Chi-X y Euronext, acciones holandesas, 2007-2008) | albertjmenkveld.com, sección de publicaciones |
| 10 | **Easley, López de Prado y O'Hara 2012**, *RFS* | **una sola cosa**: la frase del resumen que diga qué predice VPIN (buscar "toxicity" y "volatility"), y **confirmar que no reclama predecir la DIRECCIÓN del precio** | página de López de Prado (quantresearch.org) o de O'Hara (Cornell) |
| 3 | **Chordia, Roll y Subrahmanyam 2005**, *JFE* 76 | del resumen: la frase con **el horizonte en minutos** al que la predictibilidad por desbalance de órdenes desaparece (buscar "minutes" y "converge") | página de Subrahmanyam (UCLA Anderson) o de Chordia (Emory) |
| 4 | **Chordia, Roll y Subrahmanyam 2008**, *JFE* 87 | del resumen: la frase sobre **la tendencia** de la predictibilidad de corto plazo a lo largo del tiempo (buscar "predictability" y "declined") | idem |

---

# ESTADO — segunda vuelta, 2026-09-05. Tres salieron, tres no.

| # | ítem | resultado |
|---|---|---|
| 6 | Menkveld 2013 | **LEÍDO** (Tinbergen DP 11-076): €0,88 por operación = €1,55 de diferencial − €0,68 de posición; pérdida de posición negativa en todas las acciones; Sharpe 9,35 → **`L13`, la lectura más importante de las diez** |
| 5 | Brogaard, Hendershott y Riordan 2014 | **LEÍDO** (`HFT-PD.pdf`, Berkeley Haas): resumen completo textual → **`L14`**; `D18` §2 deja de ser de memoria en esa fila |
| 10 | VPIN | **LEÍDO**, resumen del propio autor en quantresearch.org, **no el paper de la RFS**: *"direction"* no aparece; *"VPIN is not a volatility forecasting model"* → **`L15`, cerrada** |
| 2 | Baron, Brogaard, Hagströmer y Kirilenko 2019 | **NO ACCESIBLE: sólo en SSRN, bloqueado** |
| 3, 4 | Chordia, Roll y Subrahmanyam 2005 y 2008 | **NO ACCESIBLE: sin copia abierta en la página del autor ni en repositorio institucional** |

**Sobre los tres que faltan, y si vale una tercera vuelta:** los tres son de acciones, no del ES, y por
`F13` pesan menos, como dijo Roberto. **Ningún veredicto de la casa depende de ellos.** Lo único que
afinarían: Baron et al. daría la ganancia por contrato de la alta frecuencia **en el E-mini** para la
tabla de Sharpes de `L13` §7 —el único comparador que sería de nuestro instrumento—. **Si se intenta, la
frase es una sola:** en el resumen o la introducción, la oración con *"per contract"* o *"profits"* que
separe agresivos de pasivos; por el lado de la revista (*JFQA* 54(3), 2019) o de la página de
Hagströmer. **Chordia no hace falta: `L14` ya cubre el mecanismo con texto.**

**Lo que NO está en la lista y por qué:** Scholtus et al. lo conseguí por Tinbergen; Andersen y
Bollerslev 1998 es un PDF escaneado que tampoco Roberto puede leer en texto; Kirilenko, Coughlan-Orlov,
Fett-Haynes, Haynes-Roberts, Onur-Reiffen y los de latencia ya están en texto.

**Formato de vuelta que sirve:** para cada ítem, las frases textuales con el número, y la página. No
hace falta resumir: la interpretación es trabajo de esta ventana y así queda la frontera limpia.

**Costos:** dinero cero, cartuchos cero, K en 261. Tiempo de Roberto: el de leer diez páginas, que es
exactamente lo que ofreció.
