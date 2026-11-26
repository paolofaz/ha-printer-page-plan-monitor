"""Test storage deduplication using the real BillingStore and a fake HA Store."""
import importlib.util
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch

class BillingStoreTests(unittest.IsolatedAsyncioTestCase):
    async def test_unchanged_state_is_not_written_and_changes_are_saved(self):
        root = Path(__file__).resolve().parents[1] / "custom_components/printer_page_plan_monitor"
        pkg = types.ModuleType("_printer_test")
        pkg.__path__ = [str(root)]
        const = types.ModuleType("_printer_test.const")
        const.DOMAIN = "printer_page_plan_monitor"
        core = types.ModuleType("homeassistant.core")
        core.HomeAssistant = object
        storage = types.ModuleType("homeassistant.helpers.storage")
        class Store:
            def __class_getitem__(cls, item):
                return cls
            def __init__(self, *args):
                self.saved = []
            async def async_save(self, data):
                self.saved.append(dict(data))
            async def async_load(self):
                return self.saved[-1] if self.saved else None
            async def async_remove(self):
                self.saved.clear()
        storage.Store = Store
        modules = {"_printer_test": pkg, "_printer_test.const": const,
                   "homeassistant": types.ModuleType("homeassistant"),
                   "homeassistant.core": core, "homeassistant.helpers": types.ModuleType("homeassistant.helpers"),
                   "homeassistant.helpers.storage": storage}
        with patch.dict(sys.modules, modules):
            spec = importlib.util.spec_from_file_location("_printer_test.storage", root / "storage.py")
            mod = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = mod
            spec.loader.exec_module(mod)
            store = mod.BillingStore(None, "test")
            state = mod.BillingState(10, "2026-11-01", "2026-12-01", 50, 40, 10, 10)
            await store.save(state)
            await store.save(state)
            self.assertEqual(len(store._store.saved), 1)
            state.last_counter = 11
            await store.save(state)
            self.assertEqual(len(store._store.saved), 2)
            await store.load()
            await store.save(state)
            self.assertEqual(len(store._store.saved), 2)
            await store.delete()
            await store.save(state)
            self.assertEqual(len(store._store.saved), 1)
