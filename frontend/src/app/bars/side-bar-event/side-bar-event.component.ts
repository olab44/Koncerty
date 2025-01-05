import { Component, Input } from '@angular/core';
import { FormsModule } from '@angular/forms'
import { TranslateModule } from '@ngx-translate/core';
import { BackendService } from '../../services/backend-connection/backend.service';
import { SessionStateServiceService } from '../../services/session-state/session-state-service.service';

@Component({
  selector: 'app-side-bar-event',
  standalone: true,
  imports: [FormsModule, TranslateModule],
  templateUrl: './side-bar-event.component.html',
  styleUrl: './side-bar-event.component.css'
})
export class SideBarEventComponent {
  @Input() isEditAvailable: boolean = false
  event!: any
  editMessage = ""

  constructor(private backend: BackendService,private state: SessionStateServiceService) {
    this.state.currentEvent.subscribe((event) => {
      this.event = event;
    });
  }

  // saveEventInfo() {
  //   this.state.setGroup(this.event);
  //   const request = {group_id: this..group_id, name: this.editGroup.group_name, extra_info: this.editGroup.extra_info}
  //   console.log(request)
  //   this.backend.postRequest('groups/editGroup', request).subscribe({
  //     next: res => {
  //       this.editMessage = "Group info saved."
  //       setTimeout(() => {
  //         this.editMessage = '';
  //       }, 5000);
  //     },
  //     error: e => {
  //       console.log(e)
  //     }
  //   })
  // }

}
