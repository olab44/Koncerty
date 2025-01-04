import { Component, EventEmitter, Output } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { TranslateModule } from '@ngx-translate/core';
import { BackendService } from '../../services/backend-connection/backend.service';

@Component({
  selector: 'app-overlay-create-group',
  standalone: true,
  imports: [FormsModule, TranslateModule],
  templateUrl: './overlay-create-group.component.html',
  styleUrl: './overlay-create-group.component.css'
})
export class OverlayCreateGroupComponent {
  @Output() close = new EventEmitter<void>()
  createMessage = "..."
  nameInput: string = ""

  constructor(private backend: BackendService) {}

  createGroup(name: string, description: string): void {
    const createGroupData = {
      parent_group: null,
      name,
      extra_info: description
    };

    this.backend.postRequest('groups/createGroup', createGroupData).subscribe({
      next: res => {
        this.createMessage = `Group ${name} created successfully.`
      },
      error: e => {
        console.log(e)
        this.createMessage = e.detail || "Unexpected error occured."
      }
    })
  }

  closeOverlay() {
    this.close.emit()
}
}
