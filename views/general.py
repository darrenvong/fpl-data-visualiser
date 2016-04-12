# -*- coding: utf-8 -*-

"""
This module is responsible for generating the generic, shared HTML contents across
all pages
@author: Darren Vong
"""

def get_navbar():
    return """<nav class="navbar">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
              <span class="sr-only">Toggle navigation</span>
              <span class="icon-bar"></span>
              <span class="icon-bar"></span>
              <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="index">Data Visualiser</a>
        </div>
        <div id="navbar" class="navbar-collapse collapse">
          <ul class="nav navbar-nav">
            <li><a href="index">Home</a></li>
            <!-- <li><a href="#">About</a></li> -->
            <li class="dropdown">
              <a href="#" id="tools-dd" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">
                Tools
                <span class="caret"></span>
              </a>
              <ul class="dropdown-menu">
                <li><a href="profile">Player profiles</a></li>
                <li><a href="head_to_head">Head-to-head comparator</a></li>
                <li><a href="player_filter">Player filter</a></li>
              </ul>
            </li>
          </ul>
        </div>
      </div>
    </nav>"""

def get_footer():
    return """<footer class="footer">
        <p>&copy; Darren Vong 2016</p>
      </footer>"""