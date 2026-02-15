import shlex
import sys

from prettytable import PrettyTable

from valutatrade_hub.core.exceptions import TradeHubError
from valutatrade_hub.core.usecases import AuthManager, TradingService
from valutatrade_hub.core.utils import validate_amount
from valutatrade_hub.parser_service.updater import RatesUpdater


class TerminalInterface:
    def __init__(self):
        self.auth_manager = AuthManager()
        self.current_user = None
        self.trader = None

    def start(self):
        print("=== ValutaTrade Hub v1.0 ===")
        print("Type 'help' for commands.")
        
        while True:
            try:
                cmd_str = input(">>> ").strip()
                if not cmd_str:
                    continue
                
                parts = shlex.split(cmd_str)
                cmd = parts[0].lower()
                args = parts[1:]

                if cmd == "exit":
                    print("Goodbye!")
                    sys.exit(0)
                elif cmd == "help":
                    self._print_help()
                elif cmd == "register":
                    self._handle_register(args)
                elif cmd == "login":
                    self._handle_login(args)
                elif cmd == "update-rates":
                    self._handle_update()
                
                # Команды требующие авторизации
                elif self.current_user:
                    if cmd == "show-portfolio":
                        self._show_portfolio()
                    elif cmd == "buy":
                        self._handle_buy(args)
                    elif cmd == "get-rate":
                        self._show_rates()
                    elif cmd == "logout":
                        self.current_user = None
                        print("Logged out.")
                    else:
                        print("Unknown command.")
                else:
                    print("Please login first.")

            except TradeHubError as e:
                print(f"[Error] {e}")
            except Exception as e:
                print(f"[System Error] {e}")

    def _print_help(self):
        print("Commands: register <user> <pass>, login <user> <pass>, update-rates")
        if self.current_user:
            print("Auth commands: show-portfolio, buy <curr> <amount_usd>, get-rate, logout")

    def _handle_register(self, args):
        if len(args) != 2:
            print("Usage: register <username> <password>")
            return
        user = self.auth_manager.register(args[0], args[1])
        print(f"User {user.username} registered!")

    def _handle_login(self, args):
        if len(args) != 2:
            print("Usage: login <username> <password>")
            return
        self.current_user = self.auth_manager.login(args[0], args[1])
        self.trader = TradingService(self.current_user)
        print(f"Welcome back, {self.current_user.username}!")
        # Имитация стартового бонуса для проверки
        usd_wallet = self.trader.pf.get_wallet("USD")
        if usd_wallet.balance == 0:
            usd_wallet.deposit(1000)
            print("Bonus: +1000 USD added.")
            self.trader._save_portfolio()

    def _show_portfolio(self):
        total, details = self.trader.get_portfolio_value()
        t = PrettyTable(["Currency", "Balance", "Est. USD"])
        for curr, bal, val in details:
            t.add_row([curr, f"{bal:.2f}", f"${val:.2f}"])
        print(t)
        print(f"Total Value: ${total:.2f}")

    def _handle_buy(self, args):
        if len(args) != 2:
            print("Usage: buy <currency> <amount_in_usd>")
            return
        curr = args[0].upper()
        amt = validate_amount(args[1])
        received = self.trader.buy_currency(curr, amt)
        print(f"Bought {received:.2f} {curr}")

    def _handle_update(self):
        updater = RatesUpdater()
        updater.run_update()
        print("Rates updated via Parser Service.")

    def _show_rates(self):
        t = PrettyTable(["Currency", "Rate (per 1 USD)"])
        for curr, rate in self.trader.rates.items():
            t.add_row([curr, rate])
        print(t)