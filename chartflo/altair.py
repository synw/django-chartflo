import os
from goerr import Err

err = Err()


def get_altair_tag_(slug):
    """
    Get the Altair tag for a chart
    """
    html = '<div id="' + slug + '"></div>\n'
    return html


def get_altair_script_(chart_obj, slug):
    """
    Get the script for an Altair chart
    """
    try:
        json_data = chart_obj.to_json(indent=0)
    except Exception as e:
        err.err(e)        
    html = '<script type="text/javascript">'
    html += 'var spec = ' + json_data.replace("\n", "") + ";"
    html += """
    var embed_opt = {"mode": "vega-lite"};
    function showError(el, error){
        el.innerHTML = ('<div class="error">'
                        + '<p>JavaScript Error: ' + error.message + '</p>'
                        + "<p>This usually means there's a typo in your chart specification. "
                        + "See the javascript console for the full traceback.</p>"
                        + '</div>');
        throw error;
    };\n"""
    html += "var el = document.getElementById('" + slug + "');"
    html += "vegaEmbed('#" + slug + "', spec, embed_opt)"
    html += ".catch(error => showError(el, error));"
    html += '</script>'
    return html


def write_file(slug, folderpath, html):
    """
    Writes a chart's html to a file
    """
    # check directories
    if not os.path.isdir(folderpath):
        try:
            os.makedirs(folderpath)
            print("Creating directory " + folderpath)
        except Exception as e:
            err.err(e)
            return
    # construct file path
    filepath = folderpath + "/" + slug + ".html"
    # write the file
    try:
        filex = open(filepath, "w")
        filex.write(html)
        filex.close()
        print("File written to", filepath)
    except Exception as e:
        err.err(e)
    return filepath


def save_altair_chart(chart_obj, slug, dashboard_slug):
    """
    Workaround for https://github.com/synw/django-chartflo-demo/issues/3
    to save separatly the Altair script and tag for a chart
    """
    tag = get_altair_tag_(slug)
    script = get_altair_script_(chart_obj, slug)
    path = "templates/dashboards/" + dashboard_slug
    write_file(slug, path + "/charts", tag)
    write_file(slug, path + "/altair_scripts", script)
    print("Altair chart saved")
    
