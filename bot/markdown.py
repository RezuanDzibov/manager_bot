from aiogram.utils import markdown as md


async def format_product_data(data: dict):
    to_return = list()
    for field_name, field_value in data.items():
        if field_name == "sizes":
            sizes = field_value
            sizes_data = list()
            for size in sizes:
                size_data = md.text(
                    *[
                        "\t" * 5 + md.text(f"{size_field_name}:", size_field_value)
                        for size_field_name, size_field_value in size.items()
                    ],
                    sep="\n"
                )
                sizes_data.append(size_data)
            sizes = md.text(*sizes_data, sep="\n" + "-" * 70 + "\n")
            to_return.append("Размеры:\n" + sizes)
            continue
        to_return.append(md.text(f"{field_name}:", field_value))
    return md.text(*to_return, sep="\n")
