import { Component } from '@angular/core';
import { TranslateModule } from '@ngx-translate/core';
import { TopBarComponent } from '../bars/top-bar.component';
import { SideBarComponent } from '../bars/side-bar.component';

@Component({
  selector: 'app-group-control',
  standalone: true,
  imports: [TranslateModule, TopBarComponent, SideBarComponent],
  templateUrl: './group-control.component.html',
  styleUrl: './group-control.component.css'
})
export class GroupControlComponent {
  group: any

  constructor() {
    this.group = history.state.group;
  }
}
