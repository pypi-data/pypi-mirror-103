import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { requestAPI } from './handler';

/**
 * Initialization data for the jupyterlab-snapshot extension.
 */
const extension: JupyterFrontEndPlugin<void> = {
  id: 'jupyterlab-snapshot',
  autoStart: true,
  activate: (app: JupyterFrontEnd) => {
    console.log('JupyterLab extension jupyterlab-snapshot is activated!');

    requestAPI<any>('snapshot/get_example')
      .then(data => {
        console.log(data);
      })
      .catch(reason => {
        console.error(
          `The jupyterlab-snapshot server extension appears to be missing.\n${reason}`
        );
      });
  }
};

export default extension;
