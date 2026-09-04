# VENTANA G — PARTE 1: DATOS CRUDOS DE PAGINAS OFICIALES
Fecha de lectura de todo lo de abajo: 2026-09-03. Solo dominios oficiales de cada firma.
Lo que no aparece aca es NO SE DETERMINA.

DEUDA DECLARADA (2026-09-04): la COMISION por operacion nunca se leyo de una fuente oficial, ni de
una firma ni de un broker. Los $2,50 por micro que usa toda la VENTANA G son HIPOTESIS heredada de
aritmetica.py; solo la mitad de deslizamiento (1 tick) tiene respaldo medido.

## APEX TRADER FUNDING  (apextraderfunding.com)
Productos NUEVOS (posteriores al 2026-03-01). Los "legacy" son otro producto y no se miden aca.

Eval INTRADAY TRAIL — https://apextraderfunding.com/help-center/intraday-trailing-drawdown-accounts/intraday-trailing-drawdown-evaluations/
  25K: objetivo $1.500 | maxDD $1.000 intradia trailing | 4 mini/40 micro | sin DLL | min dias 1 | 30 dias de acceso
  50K: objetivo $3.000 | maxDD $2.000 intradia trailing | 6 mini/60 micro | sin DLL | min dias 1 | 30 dias de acceso
  Cita: "The Intraday Trailing Threshold defines the lowest allowable account balance at any moment during
  the trading session. The threshold moves in real time based on the account's highest achieved balance
  (Peak Balance) and never moves downward."

Eval EOD TRAIL — https://apextraderfunding.com/help-center/eod-trailing-drawdown-accounts/eod-evaluations/
  25K: objetivo $1.500 | maxDD $1.000 EOD | DLL $500  | 4 contratos | min dias 1
  50K: objetivo $3.000 | maxDD $2.000 EOD | DLL $1.000 | 6 contratos | min dias 1
  Consistencia en la EVAL: "Not Applied"

Precio (widget oficial de la home, https://apextraderfunding.com/, leido 2026-09-03)
  25K Intraday: $167,00 unico  (la propia pagina muestra "$16.70 - (with Coupon Code)")
  50K Intraday: $249,00 unico  (la propia pagina muestra "$24.90 - (with Coupon Code)")
  "ONE-TIME FEE. NO REBILL. EVAL ACTIVE FOR 30 DAYS. WILL EXPIRE AFTER 30 DAYS. NO RESETS."
RESET: "Reset Fee: N/A" — no existe reset. Si toca el DD, se compra una eval nueva.
  https://apextraderfunding.com/help-center/billing/evaluation-plan-fees-and-access-explained/
ACTIVACION PA: "One-Time Activation Fee $59" (opcion Standard; existe variante "No Activation Fee" mas cara)
  https://apextraderfunding.com/help-center/billing/pa-activation-process-deadline-explained/

Primer retiro (PA Intraday) — https://apextraderfunding.com/help-center/intraday-trailing-drawdown-accounts/intraday-trailing-drawdown-payouts/
  Split 100% al trader. Minimo de retiro $500. Maximo 6 retiros por PA y despues la PA se cierra.
  25K: 5 dias con >= $100 c/u | safety net $26.100 | saldo minimo para pedir $26.600 | retiro #1 tope $1.000
  50K: 5 dias con >= $200 c/u | safety net $52.100 | saldo minimo para pedir $52.600 | retiro #1 tope $1.500
  Consistencia 50% SI aplica en la PA: ningun dia puede ser >= 50% del profit desde el ultimo retiro.
AUTOMATIZACION: NO. Prohibida por completo -> las preguntas de "propia vs terceros" y "mismo bot en otra
  firma" no aplican (N/A).

## TOPSTEP  (topstep.com / help.topstep.com) — leido 2026-09-03
Precio Trading Combine (https://help.topstep.com/en/articles/14289835-topstep-pricing-and-payment-questions)
  50K  $49/mes (via Standard) | 100K $99/mes | 150K $199/mes
  Via "No Activation Fee": 50K $95/mes, 100K $149/mes, 150K $229/mes
  DISCREPANCIA: https://www.topstep.com/no-activation-fee dice 50K $85/mes y 150K $199/mes. Dos paginas
  oficiales no coinciden. Para la aritmetica se usa la via Standard, que no depende de esto.
RESET: "Same as Trading Combine monthly costs" -> 50K = $49. Ademas cada rebill mensual da 1 reset gratis.
  https://intercom.help/topstep-llc/en/articles/8284128-what-is-the-reset
ACTIVACION: "$149 Activation Fee charged once per Express Funded Account (XFA) earned" (via Standard); $0 en la otra via.
OBJETIVO 50K: $3.000 — https://help.topstep.com/en/articles/8284208-what-is-the-consistency-target
  (la pagina da el ejemplo "$1,200 best day / $2,800 total profit" y fija el mejor dia recomendado en "<$1,500",
   que es el 50% de $3.000)
MAX LOSS LIMIT (https://help.topstep.com/en/articles/8284204-what-is-the-maximum-loss-limit)
  50K $2.000 | 100K $3.000 | 150K $4.500
  TIPO: trailing EOD pero se toca en tiempo real. Cita: "monitored in real time throughout the session" y
  "updates at the end of each trading day"; "rises as your end-of-day balance grows, but never moves down";
  se congela cuando llega al saldo inicial. Cuenta el P&L NO REALIZADO.
DAILY LOSS LIMIT: 50K $1.000 | 100K $2.000 | 150K $3.000 — OPCIONAL en el Combine y en la XFA, automatico en Live.
  https://help.topstep.com/en/articles/10490293-daily-loss-limit-in-the-trading-combine-and-express-funded-account
DIAS MINIMOS DE OPERACION en el Combine: ninguno (la FAQ oficial pregunta "Can I pass the Trading Combine in one day?")
CONSISTENCIA: el mejor dia debe quedar bajo el 50% del objetivo, si no el objetivo SUBE.
PRIMER RETIRO (https://help.topstep.com/en/articles/8284233-topstep-payout-policy)
  XFA via Standard: "5 winning days of $150+ Net P&L". Minimo de retiro $125. Split 90/10 al trader.
  Tope por pedido en 50K: $2.000 (Standard) / $3.000 (Consistency). Sin cuota mensual despues de pasar.
CUOTA MENSUAL DE LA CUENTA FONDEADA: "No monthly subscription fee after passing".
AUTOMATIZACION (releido 2026-09-03, separando las dos preguntas):
  https://help.topstep.com/en/articles/11187768-topstepx-api-access
  PROPIA: SI. "Custom automated strategies and bots are allowed via the TopstepX / ProjectX API, subject
  to standard platform rules and our prohibition on high-frequency trading (HFT)."
  TERCEROS: SI, Y LO NOMBRA EXPLICITO — es la unica de las cuatro releidas que distingue las dos cosas
  por nombre: "TopstepX API Access lets advanced Traders and developers build automated strategies,
  connect third-party tools, and execute trades directly through TopstepX." Y: "If you use third-party
  tools built by others, no coding required — just plug in your credentials." Con descargo de
  responsabilidad: "Some traders connect third-party applications to the ProjectX API. If you do, it's
  at your own risk — Topstep and ProjectX don't affiliate with, endorse, or support any external vendor
  or platform offering API integrations."
  QUIEN OPERA LA CUENTA: no lo dice como regla de identidad de la cuenta. Lo que hay es una regla de
  INFRAESTRUCTURA: "All trading activity must originate from your personal device. The use of VPS, VPNs,
  and remote servers is prohibited by Topstep's Terms of Use." Y matiza que un servidor propio puede
  mirar y registrar pero no puede transmitir ordenes: "The line is order transmission: your server can
  watch and record, but it cannot trade."
  MISMO BOT EN OTRA FIRMA: NO SE DETERMINA. No se encontro clausula de exclusividad en esta pagina ni en
  https://help.topstep.com/en/articles/10296582-prohibited-conduct (releida 2026-09-03, sin coincidencias
  de "other firm"/"another firm"/"multiple firm").

## MYFUNDEDFUTURES (myfundedfutures.com) — leido 2026-09-03
Plan RAPID — https://myfundedfutures.com/plans/rapid  (tabla "FULL RULES & SPECS" de la propia pagina)
  EVAL   25K: objetivo $1.500 | Max Loss (EOD) $1.000 | sin DLL | consistencia 50% (solo eval) | min 2 dias | activacion $0
  EVAL   50K: objetivo $3.000 | Max Loss (EOD) $2.000 | sin DLL | consistencia 50% (solo eval) | min 2 dias | activacion $0
  SIM FUNDED 50K: "Max Loss Distance $2.000", "Drawdown Type: Intraday Trailing", "MLL Locks At +$100", 5 mini/50 micro
  AMBIGUEDAD leida en la MISMA pagina: la tabla de EVAL dice "Drawdown Type: EOD" y el titular dice
  "Yes, Rapid uses intraday trailing drawdown". Se toma: eval EOD, fondeada intradia.
  PAGOS 50K: buffer requerido $2.100 | minimo $500 | split 90/10 | diario | sin consistencia en la fondeada
Plan PRO — https://myfundedfutures.com/plans/pro
  EVAL 50K: objetivo $3.000 | Max Loss (EOD) $2.000 | sin DLL | consistencia 50% (solo eval) | min 2 dias | activacion $0
  PAGOS 50K: buffer $2.100 | 14 dias desde la primera operacion | split 80/20 | minimo $1.000
PRECIO (https://myfundedfutures.com/challenge, leido 2026-09-03):
  25K $145 (codigo CLUB $72,50) | 50K $209 ($104,50) | 100K $356 ($178) | 150K $463 ($231,50)
  "Charged once today. This plan does not renew and is not a subscription." Sin cuota de activacion.
RESET: NO SE DETERMINA para Rapid/Pro. Solo se encontro un "Sim Funded Reset" del plan Flex.
AUTOMATIZACION (releido 2026-09-03, separando las dos preguntas):
  https://help.myfundedfutures.com/en/articles/8444599-fair-play-and-prohibited-trading-practices
  PROPIA: SI. "Traders may make use of automated trading strategies tailored to their own specific
  settings so long as these automated tools do not aim to exploit the favorable fills offered in the
  Simulated Environment." Y: "High-frequency Trading is not allowed on our plans."
  TERCEROS: NO LO DISTINGUE. La clausula nunca nombra "third-party" ni dice si la herramienta debe estar
  hecha por el propio trader. La frase "tailored to their own specific settings" habla de la
  CONFIGURACION, no del origen del software — no queda claro si un EA comercial de un tercero,
  configurado por el trader, cumple o no.
  QUIEN OPERA LA CUENTA: SI hay una regla de identidad, pero esta en la Seccion 4 ("Device Sharing &
  Copy-Trading other Traders"), separada de la de automatizacion: "Each individual trader is required to
  maintain their own individual trading activity. Meaning, entering, exiting and cancelling their own
  trade executions. Traders are not permitted to copy trade one another by entering, exiting or
  cancelling trade positions." Y: "Each individual trader may not use the same device (tablet, phone or
  computer) as used by another trader." Esto prohibe que OTRA PERSONA opere tu cuenta o que compartas el
  dispositivo; no dice nada sobre si un bot de terceros corriendo en TU dispositivo cuenta como que "vos"
  seguis ejecutando la operacion.
  MISMO BOT EN OTRA FIRMA: NO SE DETERMINA. No se encontro clausula de exclusividad en esta pagina.

## LUCID TRADING (lucidtrading.com) — leido 2026-09-03
LucidPro EVAL (widget oficial de la home)
  25K: objetivo $1.250 | Max Loss Limit $1.000 | tipo EOD | DLL $600 | 2 mini/20 micro | activacion GRATIS
       precio unico $123 -> $90,60 -> $70,60 con cupon | Reset $70 | "Pass in as little as one day"
  50K: objetivo $3.000 | Max Loss Limit $2.000 | tipo EOD | DLL $1.200 | 4 mini/40 micro | activacion GRATIS
       precio unico $192 -> $140,40 -> $115,40 con cupon | Reset $115 | "Pass in as little as one day"
PAGOS (https://support.lucidtrading.com/en/articles/12890092-lucidpro-payouts)
  Split 90/10. Buffer = Max Loss Limit inicial + $100. Minimo de retiro $500. Consistencia 40%.
  Objetivo minimo de ganancia entre ciclos: $250 (25K) / $500 (50K)
  25K: buffer $26.100 | saldo minimo para $500 = $26.600 | primer retiro maximo $1.000
  50K: buffer $52.100 | saldo minimo para $500 = $52.600 | primer retiro maximo $2.000
AUTOMATIZACION: https://support.lucidtrading.com/en/articles/11404728-other-activities
  PROPIA Y TERCEROS: SI, Y NO LO DISTINGUE. La firma nombra explicitamente herramientas de terceros
  ("trade copiers") en la misma frase que "sistemas automatizados", sin exigir que sean propios:
  "Automated trading systems and trade copiers are permitted. All automated activity must comply with
  Lucid Trading rules. Traders are fully responsible for any software errors, malfunctions, or unintended
  outcomes." A diferencia de Tradeify, no exige prueba de propiedad exclusiva del bot.
  MISMO BOT EN OTRA FIRMA: NO SE DETERMINA. No se encontro clausula de exclusividad.

## FUNDEDNEXT FUTURES (fundednext.com) — leido 2026-09-03
Plan FLEX (el mas barato; el tamano mas chico de Flex es 50K, no hay 25K en Flex)
  https://fundednext.com/futures/flex y https://fundednext.com/general-rules/futures/trading-objectives
  50K: objetivo $2.500 | Max Loss Limit (EOD) $1.500 | sin DLL | consistencia 40% | 3 mini/30 micro
  Precio 50K $69,99 (lista $133,99, codigo FNFLEX) | 100K $129,99 | 150K $249,99 | "One-time challenge fee"
  RESET: "Reset available from $77.99" (el $278,99 que figura corresponde al 150K)
  Sin cuota de activacion ni mensual.
  Cita del tipo de DD: "The MLL is calculated on the highest end-of-day balance. It trails up as the account
  hits new closing highs, locks once it reaches the initial balance"
25K existe solo en Rapid Pro / Rapid Daily / Legacy: objetivo $1.500, MLL $1.000 EOD, DLL none / $500.
  PRECIO del 25K: NO SE DETERMINA (Rapid y Bolt dejaron de venderse el 2026-07-10 segun la propia FAQ).
PRIMER RETIRO Flex 50K
  https://helpfutures.fundednext.com/en/articles/14878865-what-are-the-performance-reward-eligibility-criteria-for-flex-fundednext-account
  5 dias benchmark de $200 c/u | ganancia minima $500 | retiro minimo $250 | maximo 50% del profit, tope $1.500
  Reward share 95% | el MLL se fija en $50.100 tras el primer retiro | tras 5 retiros la cuenta se concluye
AUTOMATIZACION (releido 2026-09-03, separando las dos preguntas):
  https://fundednext.com/futures-challenge-terms , clausula 2.2.6 (correccion de transcripcion: la
  version anterior de esta nota decia "violating", el texto real de la pagina dice "violate")
  PROPIA Y TERCEROS: NO LO DISTINGUE. La clausula 2.2.6 no dice de quien es el bot: "Using automated
  trading bots, artificial intelligence, or ultra-high-speed execution strategies is allowed. Fair
  trading conditions must be maintained for all participants. Automated systems that violate trading
  policies will be identified and disabled. In any event FundedNext can ask the customer to share the
  system used to execute trades for review and customer is obliged to share necessary materials to
  facilitate it." No hay clausula de "sole owner" ni de "third-party" en ningun lado del documento.
  QUIEN OPERA LA CUENTA: SI hay una regla de identidad, en una clausula DISTINTA (2.1.3): "sharing account
  credentials with a third party for account management purposes is strictly prohibited." Y (2.2.5):
  "Replicating trades from another trader or coordinating trading activities among multiple accounts is
  strictly forbidden. The Customer must operate independently and make their own trading decisions."
  Esto prohibe delegar la cuenta a otra PERSONA o copiar trades de otro trader; no dice nada sobre si
  correr un bot de un tercero en tu propia cuenta cuenta como que "vos" segus operando.
  MISMO BOT EN OTRA FIRMA: NO SE DETERMINA. Lo unico sobre "otras firmas" que se encontro es sobre
  hedging, no sobre bots (clausula 1.2.20): "Cross-account hedging within FundedNext or with other firms
  is not allowed."

## BLUSKY TRADING (blusky.pro)
OJO: bluskytrading.com esta EN VENTA en GoDaddy y no es de la firma. El dominio oficial es blusky.pro.
Plan LAUNCH 50K (widget oficial de blusky.pro, leido 2026-09-03). El tamano mas chico ofrecido es 50K.
  Precio: "$59 / 30 Days" mas "+$99 at Launch" -> suscripcion de 30 dias mas cuota de $99 al pasar
  FASE 1 EVAL:   objetivo $3.000 | drawdown "-$2.000 Trailing (EOD)" | consistencia 50% | 2 dias
  FASE 2 BUFFER: objetivo $3.000 | drawdown "-$2.000 Trailing (EOD)" | consistencia 34%
  FASE 3 SIM FUNDED: saldo inicial +$3.000 | 5 mini/50 micro | pagos diarios | retiro minimo $250 | split 90/10
  BROKERAGE: saldo minimo $1.000 | split 90% al trader
  Cita EOD: "the 50K evaluation starts with a 48K minimum balance (trailing by $2000)... it does not decrease
  with losses, and is calculated from your starting balance at 6PM."
  Cuota de $99: "Launch and Stocks plans carry a one-time Launch Fee that becomes due the moment you pass"
RESET: "50K Launch Evaluation Reset Price is $49". BluLive/Buffer: $250 los primeros tres, luego sube $50 cada tres.
  https://help.blusky.pro/en/articles/12434092-resets
DRAWDOWN ESTATICO de la Sim Funded: NO SE DETERMINA (la pagina dice "static drawdown" sin dar el numero).
AUTOMATIZACION (releido 2026-09-03, separando las dos preguntas):
  https://help.blusky.pro/en/articles/12069208-ethical-trading-conduct-policy-blusky-trading-company
  PROPIA: NO SE DETERMINA. Ninguna clausula autoriza ni prohibe expresamente correr un sistema propio.
  Lo unico que toca automatizacion es una prohibicion de uso ABUSIVO, dentro de "Coordinated
  Manipulation": "using automated software (AI, ultra-high speed, bulk data entry) to unfairly influence
  outcomes". No dice que la automatizacion en si este prohibida, solo la que busca ventaja injusta.
  TERCEROS: NO SE DETERMINA Y NO LO DISTINGUE. La pagina nunca nombra "third-party" en relacion a
  software de trading. Lo mas cercano es "Account Mirroring: Copying trades from another trader, account,
  or signal provider, as this undermines independent trading skill development and risk management" —
  esto es sobre copiar las OPERACIONES de otro trader o señal, no sobre software de terceros en general.
  QUIEN OPERA LA CUENTA: SI hay una clausula, pero es sobre trading PARA otra persona, no sobre quien
  corre el bot: "Unauthorized Trading: Conducting trades on behalf of third parties or sharing program
  incentives without explicit, prior authorization." Esto prohibe operar la cuenta de otro (o la propia,
  para el beneficio de otro) sin autorizacion; no dice si un bot de terceros corriendo en tu propia
  cuenta, para tu propio beneficio, cuenta como "conducting trades on behalf of third parties".
  MISMO BOT EN OTRA FIRMA: NO SE DETERMINA. No se encontro ninguna clausula de exclusividad.
  Conclusion sin cambios: ninguna pagina oficial leida autoriza ni prohibe por nombre la automatizacion
  de terceros comun en BluSky.

## TAKE PROFIT TRADER (takeprofittrader.com) — leido 2026-09-03
Precios (tabla de la home): 25K $150/mes | 50K $170/mes | 75K $245/mes | 100K $330/mes | 150K $360/mes
  50K: objetivo $3.000 | 6 contratos/60 micros | "Daily Loss Limit $1100 Removed" (texto literal, ambiguo)
       "EOD Trailing Drawdown $2000"
  25K: objetivo NO SE DETERMINA (la tabla solo expuso el 50K). Su drawdown se deduce del buffer: $1.500.
  "Number of Trading Days to PRO Account: 3 Days"
  CUOTA DE LA CUENTA FONDEADA: "One Time $130 Fee"
CUENTA PRO — https://takeprofittraderhelp.zendesk.com/hc/en-us/articles/15171769361053-PRO-Account-Rules
  Drawdown INTRADIA: "The Trailing Drawdown is calculated intraday using your peak balance, which includes
  realized gains and unrealized gains... The drawdown will never exceed your starting account balance."
RETIROS — .../15172219527581-PRO-Account-Profit-Split-Withdrawal-Rules
  Split 80/20. "you must build a buffer on the account first"; buffer = el drawdown maximo.
  25K buffer $26.500 | 50K buffer $52.000 | 100K $103.000 | 150K $154.500
  Sin dias minimos hasta el primer retiro ("Minimum Days Until First Withdrawal: 0 Days").
  Monto minimo de retiro: NO SE DETERMINA.
RESET de la evaluacion: NO SE DETERMINA (solo se leyo "PRO Account Resets: Up to 3 resets").
AUTOMATIZACION: NO. Cita textual de PRO Account Rules:
  "1. No Trading bots/Algos - We do not allow any automated or bot trading of any kind.
   All trades must be manually executed by the trader."
  Prohibida por completo -> las preguntas de "propia vs terceros" y "mismo bot en otra firma" no aplican (N/A).

## TRADEIFY (tradeify.co) — leido 2026-09-03
Plan GROWTH (evaluacion, "Pass in 1 day"), precios del widget oficial:
  25K: $109 (codigo SEP $55) | objetivo $1.500 | Trailing Max Drawdown (EOD) $1.000 | sin DLL
       reset $75 (hasta 10 resets/mes) | consistencia 40% | activacion NINGUNA | 1 mini/10 micros
  50K: $165 (codigo SEP $83) | objetivo $3.000 | Trailing Max Drawdown (EOD) $2.000 | sin DLL
       reset $109 | consistencia 40% | activacion NINGUNA | 4 minis/40 micros
PAGOS GROWTH — https://help.tradeify.co/en/articles/11083796-growth-funded-account-payout-policy
  "Traders receive 90% of the payout amount requested." Consistencia 35%.
  5 o mas dias con ganancia mayor a $100 (25K) / $150 (50K)
  Saldo minimo: 25K $26.500 | 50K $53.000 | 100K $104.500 | 150K $156.500
  Retiro minimo: $250 (25K) / $500 (50K). Primer retiro maximo: $1.000 (25K) / $1.500 (50K)
AUTOMATIZACION — cita VERBATIM completa, https://help.tradeify.co/en/articles/10468318-guidelines-for-traders
  ("Bots/Algorithmic Trading"), leida 2026-09-03 y reverificada 2026-09-03:
  "At Tradeify, we allow the use of bots and algorithms under certain conditions:
   Ownership: You must be able to prove that you are the sole owner of the bot or strategy, and that no
   one else has access to or is using it. This ensures that the bot/algorithm is not being shared with
   other traders or firms.
   We scan to ensure there are no similar orders on other accounts. We will also require a live video of
   you enabling the code on your own PC.
   Exclusive Use: While you may use the bot on your personal accounts, using it across multiple firms is
   against Tradeify's policy. The bot should be solely for your own use within Tradeify.
   No High-Frequency Trading (HFT) Bots: Personal bots are allowed as long as they are not
   high-frequency trading (HFT) bots. Tradeify has specific risk measures in place to detect and monitor
   such activities.
   Compliance and Verification: Tradeify reserves the right to request information or documentation if
   our risk measures flag your account for potential violations of these guidelines."
  PROPIA: SI, con verificacion (prueba de propiedad exclusiva y video).
  TERCEROS: NO, por construccion. El texto nunca nombra "third-party" ni distingue las dos categorias por
  nombre, pero exige "sole owner", "no one else has access to or is using it" y "solely for your own use" —
  una herramienta comercial, compartida o de señales de un tercero no puede cumplir esa clausula.
  QUIEN OPERA LA CUENTA: no aparece en este texto ("your own PC" es sobre donde corre el codigo, no sobre
  quien ejecuta la operacion).
  MISMO BOT EN OTRA FIRMA: NO, EXPLICITO. "using it across multiple firms is against Tradeify's policy.
  The bot should be solely for your own use within Tradeify."
