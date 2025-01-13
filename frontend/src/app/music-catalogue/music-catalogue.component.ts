import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { TranslateModule } from '@ngx-translate/core';
import { TopBarComponent } from '../bars/top-bar/top-bar.component';
import { OverlayAddCompositionComponent } from '../overlays/overlay-add-composition/overlay-add-composition.component';
import { CompositionInfo, GroupInfo } from '../interfaces';
import { SessionStateService } from '../services/session-state/session-state.service';
import { FilterPipe } from '../pipe/filter.pipe';
import { BackendService } from '../services/backend-connection/backend.service';

@Component({
  selector: 'app-music-catalogue',
  standalone: true,
  imports: [ CommonModule, FormsModule, TranslateModule, TopBarComponent, OverlayAddCompositionComponent, FilterPipe ],
  templateUrl: './music-catalogue.component.html',
  styleUrl: './music-catalogue.component.css'
})
export class MusicCatalogueComponent {
  group!: GroupInfo
  viewedComposition: CompositionInfo | null = null
  visibleOverlayComposition = false
  searchPhrase: string = ""
  compositions: CompositionInfo[] = []
  new_file: File | null = null

  constructor(private backend: BackendService, private state: SessionStateService) {
    this.state.currentGroup.subscribe((group) => {
      this.group = group;
    });
    this.getCatalogue()
  }

  getCatalogue() {
    this.backend.getCatalogueExtra(this.group.group_id).subscribe({
      next: (res) => {this.compositions = res.found},
      error: (e) => { console.log(e) }
    })
  }

  viewComposition(composition: any): void {
    this.viewedComposition = composition
  }

  downloadFile(file_id: number): void {
    this.backend.postRequest('files/downloadFile', {file_id, parent_group: this.group.group_id}).subscribe({
      next: (res) => { console.log(res) },
      error: (e) => { console.log(e) }
    })
  }

  deleteFile(file_id: number): void {
    this.backend.deleteRequest('files/deleteFile', {file_id, parent_group: this.group.group_id}).subscribe({
      next: (res) => {
        if (this.viewedComposition) {
          this.viewedComposition.files = this.viewedComposition?.files.filter(file => file.id !== file_id)
        }
      },
      error: (e) => { console.log(e) }
    })
  }

  onFileChange(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      this.new_file = input.files[0]
    }
  }
  uploadFile(): void {
    //
    console.log(this.new_file)
    this.new_file = null
  }

  toggleOverlayComposition(): void {
    this.visibleOverlayComposition = !this.visibleOverlayComposition
  }
}
