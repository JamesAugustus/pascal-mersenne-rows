#!/usr/bin/env python3
"""Small logical cell/worker model, not an implementation of PCCPU hardware.

James Augustus. MIT license, as specified by the repository LICENSE.
A synchronous software schedule is used only to make dependencies visible.
Addresses identify records, not byte layouts or a physical memory bus.
"""
from math import comb
import json


def cell_address(row, column):
    if type(row) is not int or type(column) is not int:
        raise ValueError("integer coordinates required")
    if not 0 <= row < 2 or not 0 <= column < 3:
        raise ValueError("coordinate outside the 2 by 3 demonstration grid")
    return 1000 + row * 3 + column


class AddressModel:
    def __init__(self, n=9, k=3):
        if type(n) is not int or type(k) is not int or not 0 <= k < n:
            raise ValueError("adjacent Pascal entries require 0 <= k < n")
        self.n, self.k = n, k
        self.memory = {
            1000: dict(kind="worker", owner="A", op="coefficient", args=(n, k),
                       state="waiting", value=None),
            1001: dict(kind="worker", owner="B", op="coefficient", args=(n, k+1),
                       state="waiting", value=None),
            1002: dict(kind="worker", owner="C", op="add", sources=(1000, 1001),
                       destination=1003, state="waiting", value=None),
            1003: dict(kind="data", state="empty", value=None,
                       mathematical_address=(n+1, k+1)),
            1004: dict(kind="controller", state="running", logical_round=0,
                       event_counter=0, issue_address=None),
            1005: dict(kind="unused", state="empty", value=None),
        }
        self.events = []

    def read_value(self, address):
        cell = self.memory[address]
        if cell.get("state") not in ("done", "ready") or cell.get("value") is None:
            raise ValueError("value is not ready")
        return cell["value"]

    def step(self, order=(1000, 1001, 1002)):
        """Complete a ready set from one snapshot; a round is not a clock cycle."""
        if len(order) != 3 or set(order) != {1000, 1001, 1002}:
            raise ValueError("order must contain every worker exactly once")
        if self.memory[1004]["state"] == "done":
            return []
        effects = []
        for address in order:
            cell = self.memory[address]
            if cell["state"] != "waiting":
                continue
            if cell["op"] == "coefficient":
                effects.append((address, comb(*cell["args"])))
            elif all(self.memory[src]["state"] == "done" for src in cell["sources"]):
                effects.append((address, sum(self.read_value(src) for src in cell["sources"])))
        if not effects:
            raise RuntimeError("no ready worker; dependency or state error")
        # Commit only after the whole ready set has been evaluated.
        control = self.memory[1004]
        control["logical_round"] += 1
        produced = []
        for address, value in effects:
            cell = self.memory[address]
            cell.update(state="done", value=value)
            destination = cell.get("destination", address)
            if destination != address:
                self.memory[destination].update(state="ready", value=value)
            control["event_counter"] += 1
            control["issue_address"] = address
            event = dict(event=control["event_counter"],
                         logical_round=control["logical_round"],
                         worker=cell["owner"], address=address,
                         destination=destination, value=value)
            self.events.append(event)
            produced.append(event.copy())
        if self.memory[1003]["state"] == "ready":
            control["state"] = "done"
        return produced

    def run(self):
        while self.memory[1004]["state"] != "done":
            self.step()
        return self.read_value(1003)


def row_product(base, r, s):
    """Symbolic row-product decision. Does not expand the represented integer."""
    if any(type(x) is not int for x in (base, r, s)) or base < 2 or min(r,s) < 0:
        raise ValueError("base >= 2 and nonnegative integer rows required")
    n = r + s
    return dict(base=base, row=n, carry_free=comb(n, n//2) < base)


if __name__ == "__main__":
    model = AddressModel()
    result = model.run()
    print(json.dumps({"model":"logical software demonstration, not hardware",
                      "result":result, "events":model.events,
                      "controller":model.memory[1004],
                      "row_product_examples":[row_product(10,2,2),row_product(10,3,2)]},
                     indent=2))
