import urllib.request
import urllib.error
import json

url = "https://raw.githubusercontent.com/itdoginfo/allow-domains/main/Russia/inside-dnsmasq-nfset.lst"
prefix = "nftset=/"
suffix = "/4#inet#fw4#vpn_domains"
output_filename = "whitelist.json"
additional_domains_file = "additional_domains.txt"

def read_additional_domains():
    """Читает дополнительные домены из локального файла"""
    additional_domains = []
    try:
        with open(additional_domains_file, 'r', encoding='utf-8') as f:
            for line in f:
                domain = line.strip()
                if domain and not domain.startswith('#'):  # Игнорируем пустые строки и комментарии
                    additional_domains.append(domain)
        print(f"Загружено дополнительных доменов из файла: {len(additional_domains)}")
    except FileNotFoundError:
        print(f"Файл {additional_domains_file} не найден, пропускаем дополнительные домены")
    except Exception as e:
        print(f"Ошибка при чтении файла {additional_domains_file}: {e}")

    return additional_domains

def process_domains():
    try:
        with urllib.request.urlopen(url) as response:
            content = response.read().decode('utf-8')

        lines = content.strip().splitlines()
        domains = []

        for line in lines:
            if line.startswith(prefix) and line.endswith(suffix):
                domain = line[len(prefix):-len(suffix)]
                if domain:
                    domains.append(domain)

        # Добавляем дополнительные домены из локального файла
        additional_domains = read_additional_domains()
        domains.extend(additional_domains)

        result = {
            "version": 1,
            "rules": [
                {
                    "domain_suffix": domains
                }
            ]
        }

        with open(output_filename, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print(f"Всего доменов обработано: {len(domains)}")
        print(f"Результат сохранен в файл: {output_filename}")

        if additional_domains:
            print(f"Включено доменов из {additional_domains_file}: {len(additional_domains)}")
            print(f"Доменов из внешнего источника: {len(domains) - len(additional_domains)}")

    except urllib.error.URLError as e:
        print(f"Ошибка при загрузке данных: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    process_domains()
