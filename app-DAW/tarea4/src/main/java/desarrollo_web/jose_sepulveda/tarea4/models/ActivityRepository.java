package desarrollo_web.jose_sepulveda.tarea4.models;

import java.util.List;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

public interface ActivityRepository extends JpaRepository<Activity,Long> {
    @Query("SELECT a FROM Activity a WHERE a.fechaTermino < CURRENT_DATE")
    List<Activity> findFinished();

    @Query("SELECT a FROM Activity a WHERE a.fechaTermino < CURRENT_DATE")
    Page<Activity> findFinishedPage(Pageable pageable);
}
