package desarrollo_web.jose_sepulveda.tarea4.services;

import java.util.List;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Sort;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

import desarrollo_web.jose_sepulveda.tarea4.models.Activity;
import desarrollo_web.jose_sepulveda.tarea4.models.ActivityRepository;
import desarrollo_web.jose_sepulveda.tarea4.models.Note;
import desarrollo_web.jose_sepulveda.tarea4.models.NoteRepository;
import jakarta.transaction.Transactional;

@Service
@Transactional 
public class ActivityService {

  private final ActivityRepository activityRepo;
  private final NoteRepository noteRepo; 
  public ActivityService(ActivityRepository activityRepo, NoteRepository noteRepo) {
    this.activityRepo = activityRepo;
    this.noteRepo = noteRepo;
  }

  public ActivityDto addNote(long id, int valor) {
    Activity act = activityRepo.findById(id)
      .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND));
    Note n = new Note();
    n.setActivity(act);
    n.setValor(valor);
    noteRepo.save(n);
    Double avg = noteRepo.avgForActivity(id);
    return mapToDto(act, avg);
  }

  private ActivityDto mapToDto(Activity a, Double avg) {
    return new ActivityDto(
        a.getId(), a.getFechaInicio(), a.getSector(),
        a.getNombre(), a.getTema(), avg);
  }

  public List<ActivityDto> finished() {
    return activityRepo.findFinished().stream()
      .map(a -> new ActivityDto(
        a.getId(), 
        a.getFechaInicio(), 
        a.getSector(),
        a.getNombre(), 
        a.getTema(),
        a.getNotas().isEmpty() ? null :
            a.getNotas().stream().mapToInt(Note::getValor).average().orElse(0)
      ))
      .toList();
  }

  public Page<ActivityDto> finishedPaginated(int page, int size) {
    Pageable pageable = PageRequest.of(page, size, Sort.by("fechaInicio").descending());
    return activityRepo.findFinishedPage(pageable).map(a ->
        new ActivityDto(
            a.getId(), a.getFechaInicio(), a.getSector(),
            a.getNombre(), a.getTema(),
            a.getNotas().isEmpty() ? null :
                a.getNotas().stream().mapToInt(Note::getValor).average().orElse(0)
        )
    );
  }
}