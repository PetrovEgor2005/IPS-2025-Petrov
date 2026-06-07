from __future__ import annotations

from typing import Any


def solve_trade_tariff(params: dict[str, Any]) -> dict[str, float]:
    # Малая открытая экономика: эффект импортного тарифа на отечественный рынок.
    a = float(params["a"])
    b = float(params["b"])
    c = float(params["c"])
    d = float(params["d"])
    p_world = float(params["p_world"])
    tariff = float(params["tariff"])

    if b <= 0:
        raise ValueError("b must be positive")
    if d <= 0:
        raise ValueError("d must be positive")
    if tariff <= 0:
        raise ValueError("tariff must be positive")

    # Свободная торговля
    qd_free = a - b * p_world
    qs_free = max(0.0, c + d * p_world)
    imports_free = qd_free - qs_free

    if imports_free <= 0:
        raise ValueError(
            "imports_free must be positive (p_world must be below autarky equilibrium)"
        )

    # С тарифом. Если (p_world + tariff) поднимется выше автаркийной цены,
    # рынок закрывается: импорт = 0, действует цена закрытого равновесия.
    p_autarky = (a - c) / (b + d)
    p_domestic = min(p_world + tariff, p_autarky)
    qd_tariff = a - b * p_domestic
    qs_tariff = c + d * p_domestic
    imports_tariff = max(0.0, qd_tariff - qs_tariff)

    # Излишки
    cs_free = 0.5 * (a / b - p_world) * qd_free
    cs_tariff = 0.5 * (a / b - p_domestic) * qd_tariff
    ps_free = 0.5 * (p_world + c / d) * qs_free if qs_free > 0 else 0.0
    ps_tariff = 0.5 * (p_domestic + c / d) * qs_tariff

    # Поступления берутся только с реально ввезённого, а не с номинального клина.
    # Важно в автаркийном случае, когда imports = 0.
    tariff_revenue = tariff * imports_tariff
    consumer_loss = cs_free - cs_tariff
    producer_gain = ps_tariff - ps_free
    dwl = consumer_loss - producer_gain - tariff_revenue

    return {
        "imports_free": round(imports_free, 6),
        "qs_tariff": round(qs_tariff, 6),
        "qd_tariff": round(qd_tariff, 6),
        "imports_tariff": round(imports_tariff, 6),
        "tariff_revenue": round(tariff_revenue, 6),
        "consumer_loss": round(consumer_loss, 6),
        "producer_gain": round(producer_gain, 6),
        "dwl": round(dwl, 6),
    }
