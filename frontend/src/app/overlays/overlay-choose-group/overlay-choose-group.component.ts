import { Component, EventEmitter, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TranslateModule } from '@ngx-translate/core';
import { Router } from '@angular/router';
import { BackendService } from '../../services/backend-connection/backend.service';
import { GroupInfo, GroupInfoStructure, SubgroupInfo } from '../../interfaces';
import { SessionStateService } from '../../services/session-state/session-state.service';

@Component({
  selector: 'app-overlay-choose-group',
  standalone: true,
  imports: [CommonModule, TranslateModule],
  templateUrl: './overlay-choose-group.component.html',
  styleUrl: './overlay-choose-group.component.css'
})
export class OverlayChooseGroupComponent {
  @Output() close = new EventEmitter<void>()
  userGroups: GroupInfoStructure | undefined;

  constructor(private backend: BackendService, private router: Router, private state: SessionStateService) {
    this.backend.getGroups()
    .subscribe({
      next: res => {
        this.userGroups = res
      },
      error: e => {
        console.log(e)
      }
    })
  }

  gotoGroup(group: GroupInfo): void {
    this.state.setGroup(group);
    this.router.navigate(['group'], {state: {group}});
  }

  showSubgroupInfo(event: MouseEvent, subgroup: SubgroupInfo): void {
    event.stopPropagation()
    console.log(subgroup)
  }

  closeOverlay() {
    this.close.emit()
}
}
