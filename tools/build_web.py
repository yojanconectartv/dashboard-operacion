import sys, os, shutil, json, datetime
# Uso: python3 -I build_web.py <page/index.html> <carpeta_con_jsons> <carpeta_salida_sitio> <shim.js>
page, data_dir, out, shim = sys.argv[1:5]
os.makedirs(out + '/data', exist_ok=True)
body = open(page, encoding='utf-8').read()
stamp = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-5))).strftime('%d/%m/%Y %I:%M %p')
head = '''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Efectividad de la Operación · Conectar</title>
<style>
:root {
  --color-fg: #1c2733; --color-fg-muted: #5d6b78; --color-bg: #f4f8fb; --color-panel: #ffffff; --color-border-line: rgba(0, 40, 70, .12);
  --color-ok: #1f8a4c; --color-warn: #b7791f; --color-bad: #c0392b;
  --cds-gap-xs: 4px; --cds-gap-sm: 8px; --cds-gap-md: 14px; --cds-gap-lg: 20px; --cds-gap-xl: 28px;
  --cds-pad-xs: 4px; --cds-pad-sm: 8px; --cds-pad-md: 12px; --cds-pad-lg: 18px; --cds-pad-xl: 24px;
  --cds-radius: 10px; --cds-font-size-caption: 12px; --cds-font-size-body: 14px; --cds-font-size-heading: 16px; --cds-font-size-title: 28px;
  --cds-font-weight-medium: 600; --cds-dur-slow: .3s;
  --cds-chart-grid: rgba(0, 40, 70, .08); --cds-chart-axis: rgba(0, 40, 70, .25); --cds-chart-reference: #5d6b78; --cds-chart-muted: #aab4bb;
  --cds-surface-popover: #ffffff; --cds-border: rgba(0, 40, 70, .15); --cds-shadow-popover: 0 8px 24px rgba(0, 0, 0, .12); --cds-text-secondary: #5d6b78;
  --font-anthropic-sans: "Segoe UI", system-ui, -apple-system, Roboto, Arial, sans-serif; --font-anthropic-serif: Georgia, "Times New Roman", serif;
  color-scheme: light;
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--color-bg); color: var(--color-fg); font-family: var(--font-anthropic-sans); font-size: 14px; }
#dash-root { max-width: 1400px; margin: 0 auto; padding: 16px max(12px, env(safe-area-inset-left, 0px)) 32px max(12px, env(safe-area-inset-right, 0px)); }
.dash-skeleton { color: transparent !important; background: linear-gradient(90deg, rgba(0,60,100,.06), rgba(0,60,100,.12), rgba(0,60,100,.06)); border-radius: 8px; min-height: 1em; }
.web-foot { text-align: center; font-size: 11.5px; color: var(--color-fg-muted); margin-top: 14px; }
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.9.0/d3.min.js"></script>
<script>window.DASH_VERSION = "''' + stamp.replace(' ', '_').replace('/', '-').replace(':', '') + '''";</script>
<script>''' + open(shim, encoding='utf-8').read() + '''</script>
</head>
<body>
<div id="dash-root">
'''
foot = '''
<p class="web-foot">Actualizado el ''' + stamp + ''' (hora de Colombia) · Datos del Excel de seguimiento de la operación</p>
</div>
</body>
</html>
'''
open(out + '/index.html', 'w', encoding='utf-8').write(head + body + foot)
for f in os.listdir(data_dir):
    if f.endswith('.json'): shutil.copy(os.path.join(data_dir, f), out + '/data/' + f)
open(out + '/.nojekyll', 'w').write('')
print('sitio listo en', out, 'con', len([f for f in os.listdir(out + '/data')]), 'archivos de datos; actualizado', stamp)
