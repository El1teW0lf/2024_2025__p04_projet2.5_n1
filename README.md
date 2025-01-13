<h1 align="center">
  
  Projet de NSI N°2 : FNAP

  <img src="http://ForTheBadge.com/images/badges/built-with-swag.svg">
  <img src="https://forthebadge.com/images/badges/made-with-python.svg">
</h1>

# 👨‍💼 • Membres :
### Classe de 1ere 4, Cours de Mr Pioche
* #### Célestin → [GoldyRat](https://github.com/GoldyRat)
* #### Mateo → [El1teW0lf](https://github.com/El1teW0lf)
* #### Victor → [Herasium](https://github.com/Herasium)
* #### Benjamin → [Ben-cpu-gpu](https://github.com/Ben-cpu-gpu)

# 🧮 • TO DO LIST :
- [ ] Apprendre de tout le projet 2 et s'inspirer pour le projet 2.5
- [ ] Mettre à jour le jeu
- [ ] Correction intégrale des bugs ou potentiels bugs
- [ ] Lancement de la Partie 2 du Projet
- [ ] Ajout intégral des textures Blender
- [ ] Optimisation de tous l'ensemble des Modules
- [ ] Vérification approfondi de l'ensemble du Jeu

# Importing necessary libraries to render HTML into an image.
from bs4 import BeautifulSoup
from IPython.display import display, HTML

# The corrected HTML code provided for rendering.
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Most Used Languages</title>
  <style>
    .header {
      font: 600 18px 'Segoe UI', Ubuntu, Sans-Serif;
      fill: #fff;
      animation: fadeInAnimation 0.8s ease-in-out forwards;
    }
    @supports(-moz-appearance: auto) {
      /* Selector detects Firefox */
      .header { font-size: 15.5px; }
    }

    @keyframes slideInAnimation {
      from {
        width: 0;
      }
      to {
        width: calc(100% - 100px);
      }
    }
    @keyframes growWidthAnimation {
      from {
        width: 0;
      }
      to {
        width: 100%;
      }
    }
    .stat {
      font: 600 14px 'Segoe UI', Ubuntu, "Helvetica Neue", Sans-Serif;
      fill: #9f9f9f;
    }
    @supports(-moz-appearance: auto) {
      .stat { font-size: 12px; }
    }
    .bold { font-weight: 700; }
    .lang-name {
      font: 400 11px 'Segoe UI', Ubuntu, Sans-Serif;
      fill: #9f9f9f;
    }
    .stagger {
      opacity: 0;
      animation: fadeInAnimation 0.3s ease-in-out forwards;
    }
    #rect-mask rect {
      animation: slideInAnimation 1s ease-in-out forwards;
    }
    .lang-progress {
      animation: growWidthAnimation 0.6s ease-in-out forwards;
    }

    @keyframes scaleInAnimation {
      from {
        transform: translate(-5px, 5px) scale(0);
      }
      to {
        transform: translate(-5px, 5px) scale(1);
      }
    }
    @keyframes fadeInAnimation {
      from {
        opacity: 0;
      }
      to {
        opacity: 1;
      }
    }
  </style>
</head>
<body>
  <svg
    width="300"
    height="115"
    viewBox="0 0 300 115"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    role="img"
    aria-labelledby="descId"
  >
    <title id="titleId">Most Used Languages</title>
    <desc id="descId">A chart displaying the most used programming languages</desc>
    <rect
      data-testid="card-bg"
      x="0.5"
      y="0.5"
      rx="4.5"
      height="99%"
      stroke="#e4e2e2"
      width="299"
      fill="#151515"
      stroke-opacity="1"
    />
    <g data-testid="card-title" transform="translate(25, 35)">
      <text
        x="0"
        y="0"
        class="header"
        data-testid="header"
      >
        Most Used Languages
      </text>
    </g>
    <g data-testid="main-card-body" transform="translate(0, 55)">
      <svg data-testid="lang-items" x="25">
        <mask id="rect-mask">
          <rect x="0" y="0" width="250" height="8" fill="white" rx="5" />
        </mask>
        <rect
          mask="url(#rect-mask)"
          data-testid="lang-progress"
          x="0"
          y="0"
          width="149.99"
          height="8"
          fill="#f1e05a"
        />
        <rect
          mask="url(#rect-mask)"
          data-testid="lang-progress"
          x="249.99"
          y="0"
          width="110.01"
          height="8"
          fill="#C1F12E"
        />
        <g transform="translate(0, 25)">
          <g class="stagger" style="animation-delay: 450ms">
            <circle cx="5" cy="6" r="5" fill="#f1e05a" />
            <text data-testid="lang-name" x="15" y="10" class="lang-name">
              Python 70.00%
            </text>
          </g>
          <g transform="translate(150, 0)">
            <circle cx="5" cy="6" r="5" fill="#C1F12E" />
            <text data-testid="lang-name" x="15" y="10" class="lang-name">
              Ursina 30.00%
            </text>
          </g>
        </g>
      </svg>
    </g>
  </svg>
</body>
</html>
"""

# Displaying the HTML in an interactive cell output.
display(HTML(html_code))
