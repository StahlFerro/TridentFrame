<template>
  <div id="settings_panel" class="container" style="display: none; padding:10px;">
    <div class="content">
      <table class="table is-borderless" style="padding: 5px;" width="100%">
        <tr>
          <td>
            <a id="refresh_button" class="button is-large is-neon-cyan">
              <span class="icon is-large">
                <i class="fas fa-redo-alt"></i>
              </span>
              <span>Reload Window</span>
            </a>
          </td>
          <td>
            <a id="purge_cache_button" class="button is-large is-neon-cyan">
              <span class="icon is-large">
                <i class="fas fa-ban"></i>
              </span>
              <span>Purge Cache</span>
            </a>
          </td>
        </tr>
      </table>
    </div>
  </div>
</template>