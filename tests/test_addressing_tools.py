"""Offline regressions for address counts, bounded sampling, and CLI errors."""

from contextlib import redirect_stdout
from io import StringIO
import ipaddress
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

from scripts.network import cidr_to_hosts, subnet_calculator


ROOT = Path(__file__).resolve().parents[1]


def run_tool(name, *args):
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "network" / name), *args],
        capture_output=True,
        text=True,
        timeout=5,
    )


class CIDRHostTests(unittest.TestCase):
    def test_small_networks_match_standard_library(self):
        for cidr in (
            "192.0.2.0/28", "192.0.2.0/30", "192.0.2.0/31", "192.0.2.1/32",
            "2001:db8::/124", "2001:db8::/126", "2001:db8::/127",
            "2001:db8::1/128", "::/127", "::/128",
        ):
            with self.subTest(cidr=cidr):
                expected = list(ipaddress.ip_network(cidr).hosts())
                info = cidr_to_hosts.analyse_cidr(cidr)
                self.assertEqual(info["hosts"], expected)
                self.assertEqual(info["usable_hosts_count"], len(expected))

    def test_large_networks_use_bounded_address_samples(self):
        cases = (
            ("0.0.0.0/0", 4294967294, "0.0.0.1", "255.255.255.254"),
            ("10.0.0.0/8", 16777214, "10.0.0.1", "10.255.255.254"),
            ("2001:db8::/64", 18446744073709551615,
             "2001:db8::1", "2001:db8::ffff:ffff:ffff:ffff"),
            ("::/0", 2**128 - 1, "::1", "ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff"),
        )
        # Fail immediately if analysis starts enumerating a huge host iterator.
        with patch.object(ipaddress.IPv4Network, "hosts", side_effect=AssertionError), \
                patch.object(ipaddress.IPv6Network, "hosts", side_effect=AssertionError):
            for cidr, count, first, last in cases:
                with self.subTest(cidr=cidr):
                    info = cidr_to_hosts.analyse_cidr(cidr)
                    self.assertEqual(info["usable_hosts_count"], count)
                    self.assertEqual(len(info["hosts"]), 20)
                    self.assertEqual(str(info["hosts"][0]), first)
                    self.assertEqual(str(info["hosts"][-1]), last)
                    self.assertEqual(info["hosts"], sorted(set(info["hosts"])))

    def test_host_bits_are_normalized(self):
        info = cidr_to_hosts.analyse_cidr("192.0.2.129/25")
        self.assertEqual(info["cidr"], "192.0.2.128/25")
        self.assertEqual(info["usable_hosts_count"], 126)
        self.assertEqual(str(info["hosts"][0]), "192.0.2.129")
        self.assertEqual(str(info["hosts"][-1]), "192.0.2.254")

    def test_large_network_output_uses_full_count(self):
        output = StringIO()
        with redirect_stdout(output):
            cidr_to_hosts.print_analysis(cidr_to_hosts.analyse_cidr("2001:db8::/64"))
        self.assertIn("first 10 and last 10 of 18446744073709551615", output.getvalue())
        self.assertIn("18446744073709551595 more addresses", output.getvalue())

    def test_special_prefix_output_has_no_broadcast_or_subtraction(self):
        for cidr, count in (("192.0.2.0/31", 2), ("192.0.2.1/32", 1)):
            with self.subTest(cidr=cidr):
                info = cidr_to_hosts.analyse_cidr(cidr)
                self.assertTrue(info["broadcast_address"].startswith("N/A"))
                output = StringIO()
                with redirect_stdout(output):
                    cidr_to_hosts.print_analysis(info)
                self.assertIn(f"Usable hosts     = {count} (no network/broadcast subtraction)",
                              output.getvalue())

    def test_invalid_cidrs_raise(self):
        for cidr in ("bad", "192.0.2.0/33", "2001:db8::/129", "192.0.2.999/24"):
            with self.subTest(cidr=cidr), self.assertRaises(ValueError):
                cidr_to_hosts.analyse_cidr(cidr)

    def test_cli_large_blocks_complete(self):
        result = run_tool("cidr_to_hosts.py", "0.0.0.0/0", "2001:db8::/64")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("4294967294", result.stdout)
        self.assertIn("18446744073709551615", result.stdout)

    def test_cli_invalid_input_fails_but_valid_blocks_still_print(self):
        result = run_tool("cidr_to_hosts.py", "bad", "192.0.2.0/30")
        self.assertEqual(result.returncode, 1)
        self.assertIn("Invalid CIDR", result.stderr)
        self.assertNotIn("Traceback", result.stderr)
        self.assertIn("192.0.2.0/30", result.stdout)


class SubnetCalculatorTests(unittest.TestCase):
    def test_known_subnets_including_prefix_boundaries(self):
        cases = (
            ("192.0.2.100/24", "192.0.2.0", "192.0.2.255", 254,
             "192.0.2.1", "192.0.2.254"),
            ("192.0.2.1/30", "192.0.2.0", "192.0.2.3", 2,
             "192.0.2.1", "192.0.2.2"),
            ("192.0.2.10/31", "192.0.2.10", "N/A", 2,
             "192.0.2.10", "192.0.2.11"),
            ("192.0.2.10/32", "192.0.2.10", "N/A", 1,
             "192.0.2.10", "192.0.2.10"),
            ("192.0.2.10/0", "0.0.0.0", "255.255.255.255", 4294967294,
             "0.0.0.1", "255.255.255.254"),
        )
        for cidr, network, broadcast, count, first, last in cases:
            with self.subTest(cidr=cidr):
                ip, mask = subnet_calculator.parse_input([cidr])
                info = subnet_calculator.calculate_subnet(ip, mask)
                self.assertEqual(info["network"], network)
                self.assertEqual(info["broadcast"], broadcast)
                self.assertEqual(info["usable_hosts"], count)
                self.assertEqual(info["first_host"], first)
                self.assertEqual(info["last_host"], last)

    def test_cidr_and_dotted_mask_agree(self):
        cidr = subnet_calculator.parse_input(["10.0.0.50/20"])
        dotted = subnet_calculator.parse_input(["10.0.0.50", "255.255.240.0"])
        self.assertEqual(cidr, dotted)
        self.assertEqual(subnet_calculator.calculate_subnet(*cidr)["network"], "10.0.0.0")

    def test_bare_address_is_one_host(self):
        info = subnet_calculator.calculate_subnet(*subnet_calculator.parse_input(["192.0.2.10"]))
        self.assertEqual(info["prefix_len"], 32)
        self.assertEqual(info["usable_hosts"], 1)

    def test_invalid_masks_and_addresses_are_rejected(self):
        for address, mask in (
            ("192.0.2.1", "255.0.255.0"),
            ("192.0.2.1", "255.255.255.1"),
            ("192.0.2.1", "0.0.0.255"),
            ("192.0.2.1", "255.255.255.256"),
            ("192.0.2.999", "255.255.255.0"),
            ("2001:db8::1", "255.255.255.0"),
        ):
            with self.subTest(address=address, mask=mask):
                with self.assertRaises(ValueError):
                    subnet_calculator.calculate_subnet(address, mask)
                with self.assertRaises(ValueError):
                    subnet_calculator.parse_input([address, mask])

    def test_invalid_prefixes_are_rejected(self):
        for prefix in (-1, 33):
            with self.subTest(prefix=prefix), self.assertRaises(ValueError):
                subnet_calculator.mask_from_prefix(prefix)

    def test_cli_errors_are_actionable(self):
        for args in (("192.0.2.1/33",), ("bad",), ("192.0.2.1", "255.0.255.0")):
            with self.subTest(args=args):
                result = run_tool("subnet_calculator.py", *args)
                self.assertEqual(result.returncode, 2)
                self.assertIn("error:", result.stderr)
                self.assertNotIn("Traceback", result.stderr)

    def test_cli_single_host_output(self):
        result = run_tool("subnet_calculator.py", "192.0.2.10/32")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("/32 identifies one host address", result.stdout)
        self.assertIn("Last Address (bin)", result.stdout)


if __name__ == "__main__":
    unittest.main()
