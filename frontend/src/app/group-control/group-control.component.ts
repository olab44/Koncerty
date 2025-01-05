import { Component } from '@angular/core';
import { TranslateModule } from '@ngx-translate/core';
import { TopBarComponent } from '../bars/top-bar/top-bar.component';
import { SideBarComponent } from '../bars/side-bar/side-bar.component';
import { GroupInfo } from '../interfaces';
import { SessionStateServiceService } from '../services/session-state/session-state-service.service';

@Component({
  selector: 'app-group-control',
  standalone: true,
  imports: [TranslateModule, TopBarComponent, SideBarComponent],
  templateUrl: './group-control.component.html',
  styleUrl: './group-control.component.css'
})
export class GroupControlComponent {
  group!: GroupInfo

  constructor(private state: SessionStateServiceService) {
    this.state.currentGroup.subscribe((group) => {
      this.group = group;
    });
  }
}
