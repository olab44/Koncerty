import { Component, EventEmitter, Output } from '@angular/core';
import { TranslateModule } from '@ngx-translate/core';
import { BackendService } from '../../services/backend-connection/backend.service';

@Component({
  selector: 'app-overlay-create-group',
  standalone: true,
  imports: [TranslateModule],
  templateUrl: './overlay-create-group.component.html',
  styleUrl: './overlay-create-group.component.css'
})
export class OverlayCreateGroupComponent {
  constructor(private backend: BackendService) {}

  @Output() close = new EventEmitter<void>()
  createMessage = "..."

  createGroup(name: string, description: string): void {
    const createGroupData = {
      parent_group: null,
      name,
      extra_info: description
    };

    this.backend.postRequest('groups/createGroup', createGroupData).subscribe({
      next: res => {
        this.createMessage = "group created"
      },
      error: e => {
        console.log(e)
        this.createMessage = e.detail || "unexpected error occured"
      }
    })
  }

  closeOverlay() {
    this.close.emit()
}
}
