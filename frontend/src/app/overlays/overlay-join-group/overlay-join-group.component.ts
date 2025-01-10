import { Component, EventEmitter, Output } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { TranslateModule } from '@ngx-translate/core';
import { BackendService } from '../../services/backend-connection/backend.service';

@Component({
  selector: 'app-overlay-join-group',
  standalone: true,
  imports: [FormsModule, TranslateModule],
  templateUrl: './overlay-join-group.component.html',
  styleUrl: './overlay-join-group.component.css'
})
export class OverlayJoinGroupComponent {
  constructor(private backend: BackendService) {}

  @Output() close = new EventEmitter<void>()

  joinMessage: string = '...'
  codeInput: string = ""

  joinGroup(inv_code: string) : void {
    this.backend.postRequest('groups/joinGroup', { inv_code }).subscribe({
      next: res => {
        this.joinMessage = `Group joined successfully.`
      },
      error: e => {
        console.log(e)
        this.joinMessage = e.detail || "Unexpected error occured."
      }
    })
  }

  closeOverlay() {
    this.close.emit()
  }
}
