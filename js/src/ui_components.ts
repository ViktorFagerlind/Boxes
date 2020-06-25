'use strict'
import { Framework } from './framework';

export module UIComponents
{
    export class SideBar {
        constructor() {
        }

        public render(parent: HTMLElement)
        {
            let sidebar = Framework.div("sidebar");
            parent.append(sidebar);
        }
    }
}