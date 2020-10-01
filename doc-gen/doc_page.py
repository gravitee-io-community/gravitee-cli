from click import formatting
import click


class DocPage(object):

    def __init__(self, name, ctx, version):
        self.name = name
        self.version = version
        self.ctx = ctx

    def __str__(self):
        lines = []

        command = self.ctx.command

        formatter = formatting.HelpFormatter()

        pieces = command.collect_usage_pieces(self.ctx)
        formatter.write_usage(self.ctx.command_path, ' '.join(pieces), prefix="$ ")
        command_str = formatter.getvalue().rstrip('\n')

        lines.append("= {}\n".format(self.ctx.command_path))
        lines.append("{}\n".format(self.ctx.command.get_short_help_str()))
        lines.append("[source,shell]")
        lines.append("----")
        lines.append(command_str)
        lines.append("----\n")
        if self.ctx.command.help:
            lines.append("{}\n".format(self.ctx.command.help))

        options = [x.get_help_record(self.ctx) for x in self.ctx.command.params if isinstance(x, click.Option)]

        if options:
            lines.append("== Options\n")

            lines.append('[cols="2a*"]\n')
            lines.append('|===\n')

            for option in options:
                lines.append('2+| *{}*\n'.format(option[0].replace('|', '\|')))
                lines.append('|Description | {}\n'.format(option[1].replace('|', '\|')))

            lines.append('|===\n')

        doc_page = '\n'.join(lines)

        if not doc_page.endswith('\n'):
            doc_page += '\n'

        return doc_page
