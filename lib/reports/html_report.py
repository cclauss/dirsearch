# -*- coding: utf-8 -*-
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#  Author: Mauro Soria

import json
import os

from lib.reports import *
from lib.utils import FileUtils
from thirdparty.mako.template import Template


class HTMLReport(FileBaseReport):
    def generate(self):
        template_file = os.path.dirname(os.path.realpath(__file__)) + '/templates/html_report_template.html'
        mytemplate = Template(filename=template_file)

        metadata = {
            "command": " ".join(sys.argv),
            "date": time.ctime()
        }
        results = []
        for entry in self.entries:
            for e in entry.results:
                headerName = "{0}://{1}:{2}/{3}".format(
                    entry.protocol, entry.host, entry.port, entry.basePath
                )

                statusColorClass = ''
                if e.status >= 200 and e.status <= 299:
                    statusColorClass = 'text-success'
                elif e.status >= 300 and e.status <= 399:
                    statusColorClass = 'text-warning'
                elif e.status >= 400 and e.status <= 599:
                    statusColorClass = 'text-danger'

                results.append({
                    "url": headerName + e.path,
                    "path": e.path,
                    "status": e.status,
                    "statusColorClass": statusColorClass,
                    "contentLength": FileUtils.size_human(e.getContentLength()),
                    "contentType": e.response.headers.get("content-type"),
                    "redirect": e.response.redirect
                })

        return mytemplate.render(metadata=metadata, results=json.dumps(results))

    def save(self):
        self.file.seek(0)
        self.file.truncate(0)
        self.file.flush()
        self.file.writelines(self.generate())
        self.file.flush()
