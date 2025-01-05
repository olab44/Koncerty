import { Component, Input } from '@angular/core';
import { FormsModule } from '@angular/forms'
import { TranslateModule } from '@ngx-translate/core';
import { GroupInfo } from '../../interfaces';
import { BackendService } from '../../services/backend-connection/backend.service';
import { SessionStateService } from '../../services/session-state/session-state.service';

@Component({
  selector: 'app-side-bar',
  standalone: true,
  imports: [FormsModule, TranslateModule],
  templateUrl: './side-bar.component.html',
  styleUrl: './side-bar.component.css'
})
export class SideBarComponent {
  @Input() isEditAvailable: boolean = false
  group!: GroupInfo
  name: string = ""
  extra_info: string = ""
  editMessage = ""

  constructor(private backend: BackendService,private state: SessionStateService) {
    this.state.currentGroup.subscribe((group) => {
      this.group = group;
    });
    this.name = this.group.group_name
    this.extra_info = this.group.extra_info? this.group.extra_info : ""
  }

  onInput() {
    this.editMessage = "Info edited..."
  }

  saveGroupInfo(name: string, extra_info: string) {
    this.group.group_name = name
    this.group.extra_info = extra_info
    const request = {group_id: this.group.group_id, name: name, extra_info: extra_info}
    console.log(request)
    this.backend.postRequest('groups/editGroup', request).subscribe({
      next: res => {
        this.editMessage = "Group info saved."
        setTimeout(() => {
          this.editMessage = '';
        }, 5000);
      },
      error: e => {
        console.log(e)
      }
    })
  }

}
