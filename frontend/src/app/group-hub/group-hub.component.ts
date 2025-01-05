import { Component } from '@angular/core';
import { TranslateModule } from '@ngx-translate/core';
import { Router } from '@angular/router';
import { TopBarComponent } from '../bars/top-bar/top-bar.component';
import { SideBarComponent } from '../bars/side-bar/side-bar.component';
import { GroupInfo } from '../interfaces';
import { SessionStateServiceService } from '../services/session-state/session-state-service.service';

@Component({
  selector: 'app-group-hub',
  standalone: true,
  imports: [TranslateModule, TopBarComponent, SideBarComponent],
  templateUrl: './group-hub.component.html',
  styleUrl: './group-hub.component.css'
})
export class GroupHubComponent {
  group!: GroupInfo

  constructor(private router: Router, private state: SessionStateServiceService) {
    this.state.currentGroup.subscribe((group) => {
      this.group = group;
    });
  }

  navigate(path: string) {
    this.router.navigate(["/group", path])
  }
}
